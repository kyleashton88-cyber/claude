// Convert the master markdown file into a styled Word document.
// Usage: node build_docx.js <master.md> <out.docx>
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, AlignmentType, LevelFormat,
  PageBreak, TableOfContents, Footer, PageNumber, ExternalHyperlink,
} = require('docx');

const [src, out] = process.argv.slice(2);
let md = fs.readFileSync(src, 'utf8');

// Quiz <details> blocks -> visible question + answer (print has no click-to-reveal).
md = md.replace(/<details>\s*<summary>([\s\S]*?)<\/summary>\s*([\s\S]*?)<\/details>/g,
  (_, q, a) => `**Q: ${q.trim()}**\n\n*Answer:* ${a.trim()}\n`);
// Drop the "don't edit this file" generator note; it doesn't apply to the Word copy.
md = md.replace(/\*Generated [^\n]*\n/, '');

const ACCENT = '1F4E79';
const PAGE_W = 9026; // A4 text width in DXA (1" margins)
const MONO = 'Consolas';
let mermaidIdx = 0;
let firstH1 = true;

function inline(tokens, base = {}) {
  const runs = [];
  for (const t of tokens || []) {
    switch (t.type) {
      case 'strong': runs.push(...inline(t.tokens, { ...base, bold: true })); break;
      case 'em': runs.push(...inline(t.tokens, { ...base, italics: true })); break;
      case 'codespan': runs.push(new TextRun({ ...base, text: decode(t.text), font: MONO, size: 19, shading: { type: ShadingType.CLEAR, fill: 'EEF2F6' } })); break;
      case 'link':
        runs.push(new ExternalHyperlink({ link: t.href, children: inline(t.tokens, { ...base, color: '0563C1', underline: {} }) }));
        break;
      case 'br': runs.push(new TextRun({ ...base, break: 1 })); break;
      case 'del': runs.push(...inline(t.tokens, { ...base, strike: true })); break;
      case 'html': break;
      case 'text':
      case 'escape':
        if (t.tokens) runs.push(...inline(t.tokens, base));
        else runs.push(new TextRun({ ...base, text: decode(t.text) }));
        break;
      default: runs.push(new TextRun({ ...base, text: decode(t.raw || '') }));
    }
  }
  return runs;
}

function decode(s) {
  return s.replace(/\n/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'");
}

function cellParas(cell, header) {
  return [new Paragraph({ spacing: { before: 40, after: 40 }, children: inline(cell.tokens, header ? { bold: true, color: 'FFFFFF' } : {}) })];
}

function table(t) {
  const n = t.header.length;
  const w = Math.floor(PAGE_W / n);
  const widths = Array(n).fill(w);
  widths[n - 1] = PAGE_W - w * (n - 1);
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'BFC9D4' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const mk = (cells, header, i) => new TableRow({
    tableHeader: header,
    children: cells.map((c, j) => new TableCell({
      width: { size: widths[j], type: WidthType.DXA }, borders,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      shading: header ? { type: ShadingType.CLEAR, fill: ACCENT } : (i % 2 ? { type: ShadingType.CLEAR, fill: 'F3F6F9' } : undefined),
      children: cellParas(c, header),
    })),
  });
  return [new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, columnWidths: widths,
    rows: [mk(t.header, true, 0), ...t.rows.map((r, i) => mk(r, false, i))],
  }), new Paragraph({ spacing: { after: 120 }, children: [] })];
}

function list(t, level = 0) {
  const out = [];
  for (const item of t.items) {
    const [first, ...rest] = item.tokens;
    const prefix = item.task ? [new TextRun({ text: item.checked ? '☑ ' : '☐ ' })] : [];
    const firstRuns = first && (first.type === 'text' || first.type === 'paragraph') ? inline(first.tokens || [first]) : [];
    out.push(new Paragraph({
      numbering: item.task ? undefined : { reference: t.ordered ? 'numbers' : 'bullets', level },
      indent: item.task ? { left: 360 + level * 360 } : undefined,
      spacing: { after: 60 },
      children: [...prefix, ...firstRuns],
    }));
    for (const r of rest) {
      if (r.type === 'list') out.push(...list(r, level + 1));
      else out.push(...block(r));
    }
  }
  return out;
}

function block(t) {
  switch (t.type) {
    case 'heading': {
      const level = [null, HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4][Math.min(t.depth, 4)];
      const pageBreak = t.depth === 1 && !firstH1;
      if (t.depth === 1) firstH1 = false;
      return [new Paragraph({ heading: level, pageBreakBefore: pageBreak, children: inline(t.tokens) })];
    }
    case 'paragraph': return [new Paragraph({ spacing: { after: 120 }, children: inline(t.tokens) })];
    case 'list': return list(t);
    case 'table': return table(t);
    case 'blockquote':
      return t.tokens.flatMap(b => b.type === 'paragraph'
        ? [new Paragraph({
          indent: { left: 360 }, spacing: { after: 120 },
          border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
          shading: { type: ShadingType.CLEAR, fill: 'F3F6F9' },
          children: inline(b.tokens),
        })]
        : block(b));
    case 'code':
      if (t.lang === 'mermaid') {
        const file = path.join(__dirname, `mermaid-${mermaidIdx++}.png`);
        if (fs.existsSync(file)) {
          const buf = fs.readFileSync(file);
          const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
          const width = Math.min(260, w / 2);
          return [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
            children: [new ImageRun({ type: 'png', data: buf, transformation: { width, height: Math.round(h * width / w) } })] })];
        }
      }
      return t.text.split('\n').map((line, i, a) => new Paragraph({
        spacing: { before: i ? 0 : 60, after: i === a.length - 1 ? 160 : 0 },
        shading: { type: ShadingType.CLEAR, fill: 'EEF2F6' },
        children: [new TextRun({ text: line || ' ', font: MONO, size: 18 })],
      }));
    case 'hr': return [];
    case 'space': return [];
    case 'html': return [];
    default: return t.tokens ? [new Paragraph({ children: inline(t.tokens) })] : [];
  }
}

const tokens = marked.lexer(md);
const body = tokens.flatMap(block);

const title = [
  new Paragraph({ spacing: { before: 3000, after: 200 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'On-Chain Operator Program', bold: true, size: 56, color: ACCENT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
    children: [new TextRun({ text: 'Master File — Offer, Curriculum, Setup, Funnel & Course Content', size: 28, color: '404040' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: `Draft · ${new Date().toISOString().slice(0, 10)}`, size: 22, color: '707070' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Educational content only. Not financial advice. No results are guaranteed.', italics: true, size: 20, color: '707070' })] }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Table of Contents')] }),
  new TableOfContents('Table of Contents', { hyperlink: true, headingStyleRange: '1-2' }),
  new Paragraph({ children: [new PageBreak()] }),
];

const doc = new Document({
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: 'Calibri', size: 21 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 36, bold: true, color: ACCENT }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, color: ACCENT }, paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 24, bold: true, color: '2E2E2E' }, paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 2 } },
      { id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 22, bold: true, color: '2E2E2E' }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 3 } },
    ],
  },
  numbering: {
    config: [
      { reference: 'bullets', levels: [0, 1, 2].map(l => ({ level: l, format: LevelFormat.BULLET, text: ['•', '◦', '▪'][l], alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360 * (l + 1), hanging: 260 } } } })) },
      { reference: 'numbers', levels: [0, 1, 2].map(l => ({ level: l, format: LevelFormat.DECIMAL, text: `%${l + 1}.`, alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360 * (l + 1), hanging: 300 } } } })) },
    ],
  },
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'On-Chain Operator Program · ', size: 16, color: '808080' }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '808080' })] })] }) },
    children: [...title, ...body],
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(out, buf); console.log('wrote', out); });
