/**
 * NOVA-MIND — Generador de Estrategia Digital
 * Basado en los 9 Bloques del Business Model Canvas
 */

'use strict';

// ── Constants ──────────────────────────────────────────────────────────

const BLOCKS = ['socios', 'actividades', 'recursos', 'propuesta',
  'relaciones', 'segmentos', 'canales', 'ingresos', 'costos'];

const CONTENT_TYPES = [
  {
    label: '📚 Educativo',
    description: 'Tutoriales, guías, how-to, webinars',
    frequency: '3-4 veces/semana',
    platforms: ['Blog', 'YouTube', 'LinkedIn', 'Instagram Carrusel'],
  },
  {
    label: '🎯 Promocional',
    description: 'Casos de éxito, testimonios, demos de producto',
    frequency: '1-2 veces/semana',
    platforms: ['Instagram', 'Facebook', 'Email', 'TikTok'],
  },
  {
    label: '💬 Engagement',
    description: 'Polls, preguntas, behind-the-scenes, stories',
    frequency: 'Diario',
    platforms: ['Instagram Stories', 'Twitter/X', 'LinkedIn', 'TikTok'],
  },
  {
    label: '💎 Valor',
    description: 'Recursos gratuitos, templates, checklists, tips',
    frequency: '2-3 veces/semana',
    platforms: ['Newsletter', 'LinkedIn', 'Telegram', 'Blog'],
  },
];

const AUTOMATION_TOOLS = [
  {
    name: 'Buffer / Hootsuite',
    category: 'Publicación',
    description: 'Programa y publica contenido en múltiples redes sociales automáticamente.',
    icon: '📅',
  },
  {
    name: 'Make (Integromat) / Zapier',
    category: 'Flujos de trabajo',
    description: 'Automatiza procesos entre apps: CRM, email, redes sociales, hojas de cálculo.',
    icon: '🔄',
  },
  {
    name: 'ChatGPT / Claude',
    category: 'Creación de contenido IA',
    description: 'Genera borradores de posts, captions, emails y guiones con inteligencia artificial.',
    icon: '🤖',
  },
  {
    name: 'Canva Pro',
    category: 'Diseño',
    description: 'Crea y programa publicaciones visuales con plantillas de marca en segundos.',
    icon: '🎨',
  },
  {
    name: 'Mailchimp / ActiveCampaign',
    category: 'Email Marketing',
    description: 'Automatiza secuencias de email según el comportamiento del suscriptor.',
    icon: '📧',
  },
  {
    name: 'Notion / Airtable',
    category: 'Gestión de contenido',
    description: 'Organiza tu calendario editorial y repositorio de contenido en un solo lugar.',
    icon: '🗂️',
  },
  {
    name: 'Later / Planoly',
    category: 'Instagram & TikTok',
    description: 'Planifica el feed visual y programa reels, stories y posts con anticipación.',
    icon: '📸',
  },
  {
    name: 'Google Analytics / Meta Pixel',
    category: 'Analytics',
    description: 'Mide el rendimiento y el ROI de cada pieza de contenido publicada.',
    icon: '📊',
  },
];

const CALENDAR_ITEMS = [
  { type: 'Educativo',      platform: 'Blog/LinkedIn',     emoji: '📝' },
  { type: 'Story',          platform: 'Instagram',          emoji: '📱' },
  { type: 'Video corto',    platform: 'TikTok/Reels',       emoji: '🎥' },
  { type: 'Tip del día',    platform: 'Twitter/X',          emoji: '💡' },
  { type: 'Caso de éxito',  platform: 'LinkedIn',           emoji: '🏆' },
  { type: 'Carrusel',       platform: 'Instagram',          emoji: '🎠' },
  { type: 'Repurpose',      platform: 'Varios',             emoji: '♻️' },
  { type: 'Newsletter',     platform: 'Email',              emoji: '📧' },
  { type: 'Testimonio',     platform: 'Stories/Feed',       emoji: '⭐' },
  { type: 'Behind scenes',  platform: 'Instagram/TikTok',   emoji: '🎬' },
  { type: 'Encuesta',       platform: 'Stories',            emoji: '🗳️' },
  { type: 'Recurso gratis', platform: 'LinkedIn/Email',     emoji: '🎁' },
  { type: 'Colaboración',   platform: 'Varios',             emoji: '🤝' },
  { type: 'Repaso semanal', platform: 'Stories',            emoji: '📊' },
];

const KPI_ROWS = [
  ['👥 Segmentos de Clientes',   'Tasa de conversión por segmento',       'Google Analytics',    '> 2–3 %'],
  ['💡 Propuesta de Valor',      'NPS / satisfacción del cliente',        'Typeform / Survey',   '> 50 NPS'],
  ['📢 Canales',                 'Costo de adquisición (CAC)',            'Meta Ads / GA',       'Menor al LTV ÷ 3'],
  ['❤️ Relaciones con Clientes', 'Engagement rate',                       'Instagram Insights',  '> 3 %'],
  ['💰 Fuentes de Ingresos',     'MRR / tasa de conversión',              'Stripe / CRM',        '+10 % MoM'],
  ['💎 Recursos Clave',          'ROI por canal / herramienta',           'Spreadsheet',         '> 300 % ROI'],
  ['⚙️ Actividades Clave',       'Tiempo ahorrado por automatización',    'Toggl / Notion',      '> 5 h / semana'],
  ['🤝 Socios Clave',            'Leads generados por colaboraciones',    'UTM Links',           '> 20 % del total'],
  ['📊 Estructura de Costos',    'Costo por contenido publicado',         'Spreadsheet',         'Reducir 10 % / trimestre'],
];

// ── Helpers ────────────────────────────────────────────────────────────

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function getCanvasData() {
  const data = {};
  BLOCKS.forEach(function (id) {
    const el = document.getElementById(id);
    data[id] = el ? el.value.trim() : '';
  });
  return data;
}

function channelTags(text) {
  const map = {
    instagram: '📸 Instagram',
    tiktok:    '🎵 TikTok',
    youtube:   '▶️ YouTube',
    linkedin:  '💼 LinkedIn',
    facebook:  '👥 Facebook',
    twitter:   '🐦 Twitter/X',
    email:     '📧 Email',
    whatsapp:  '💬 WhatsApp',
    blog:      '✍️ Blog',
    podcast:   '🎙️ Podcast',
    web:       '🌐 Web',
  };

  const lower = text.toLowerCase();
  const found = Object.entries(map)
    .filter(function (entry) { return lower.includes(entry[0]); })
    .map(function (entry) { return '<span class="tag">' + entry[1] + '</span>'; });

  return found.length
    ? found.join('')
    : '<span class="tag">📢 Canales Digitales</span><span class="tag teal">🌐 Presencia Web</span>';
}

// ── Content Strategy Tab ───────────────────────────────────────────────

function buildContentStrategy(data) {
  let html = '';

  if (data.canales) {
    html += '<div class="strategy-section">'
      + '<h4>📢 Canales Digitales Identificados</h4>'
      + '<div class="strategy-card">'
      + '<h5>Tus canales actuales:</h5>'
      + '<p style="margin-bottom:.75rem;color:var(--text)">' + escapeHtml(data.canales) + '</p>'
      + '<div>' + channelTags(data.canales) + '</div>'
      + '</div>'
      + '</div>';
  }

  if (data.segmentos) {
    html += '<div class="strategy-section">'
      + '<h4>👥 Estrategia por Segmento de Cliente</h4>'
      + '<div class="strategy-card">'
      + '<h5>Tu audiencia objetivo:</h5>'
      + '<p style="margin-bottom:.75rem;color:var(--text)">' + escapeHtml(data.segmentos) + '</p>'
      + '<ul>'
      + '<li>Crea <strong>buyer personas</strong> detalladas para cada segmento</li>'
      + '<li>Adapta el lenguaje y tono a cada perfil de cliente</li>'
      + '<li>Segmenta tus campañas de email y anuncios por comportamiento</li>'
      + '<li>Analiza en qué plataformas pasa más tiempo tu audiencia</li>'
      + '</ul>'
      + '</div>'
      + '</div>';
  }

  if (data.propuesta) {
    html += '<div class="strategy-section">'
      + '<h4>💡 Contenido basado en tu Propuesta de Valor</h4>'
      + '<div class="strategy-card">'
      + '<h5>Tu propuesta de valor:</h5>'
      + '<p style="margin-bottom:.75rem;color:var(--text)">' + escapeHtml(data.propuesta) + '</p>'
      + '<ul>'
      + '<li>Crea contenido que <strong>demuestre</strong> tu propuesta en acción</li>'
      + '<li>Comparte casos de uso reales y testimonios de clientes</li>'
      + '<li>Usa el formato <em>Problema → Solución → Resultado</em></li>'
      + '<li>Publica contenido educativo sobre el problema que resuelves</li>'
      + '</ul>'
      + '</div>'
      + '</div>';
  }

  html += '<div class="strategy-section"><h4>🎯 Tipos de Contenido Recomendados</h4>';
  CONTENT_TYPES.forEach(function (ct) {
    html += '<div class="strategy-card">'
      + '<h5>' + ct.label + '</h5>'
      + '<p>' + ct.description + '</p>'
      + '<p style="margin-top:.4rem"><strong>Frecuencia:</strong> ' + ct.frequency + '</p>'
      + '<div style="margin-top:.5rem">'
      + ct.platforms.map(function (p) { return '<span class="tag">' + p + '</span>'; }).join('')
      + '</div>'
      + '</div>';
  });
  html += '</div>';

  html += '<div class="strategy-section">'
    + '<h4>🏛️ Pilares de Contenido (Regla 40-20-20-20)</h4>'
    + '<div class="strategy-card"><ul>'
    + '<li><strong>Educación (40 %):</strong> Enseña algo valioso relacionado con tu industria</li>'
    + '<li><strong>Inspiración (20 %):</strong> Motiva, comparte historias y transformaciones</li>'
    + '<li><strong>Entretenimiento (20 %):</strong> Humaniza tu marca, behind-the-scenes</li>'
    + '<li><strong>Conversión (20 %):</strong> Invita a la acción: comprar, registrarse, contactar</li>'
    + '</ul></div>'
    + '</div>';

  return html;
}

// ── Automation Tab ─────────────────────────────────────────────────────

function buildAutomation() {
  let html = '<div class="strategy-section"><h4>🔄 Flujos de Automatización Clave</h4>';

  const workflows = [
    {
      title: 'Workflow 1 – Publicación Automática',
      desc: 'Crea contenido → Aprueba en Notion → Publica automáticamente con Buffer/Later',
      steps: [
        'Conecta tu calendario editorial con Buffer o Hootsuite',
        'Configura plantillas de diseño en Canva para cada tipo de post',
        'Programa publicaciones con 1–2 semanas de anticipación',
      ],
    },
    {
      title: 'Workflow 2 – Nurturing de Leads',
      desc: 'Lead magnet → Secuencia de email → Segmentación → Oferta personalizada',
      steps: [
        'Crea un lead magnet alineado con tu propuesta de valor',
        'Configura una secuencia de 5–7 emails de bienvenida',
        'Segmenta por comportamiento: abre emails, hace clic, compra',
      ],
    },
    {
      title: 'Workflow 3 – Repurposing de Contenido',
      desc: '1 video largo → múltiples formatos → múltiples plataformas',
      steps: [
        'Graba 1 video/podcast → transcribe con Otter.ai o Whisper',
        'Convierte la transcripción en artículo de blog',
        'Extrae clips cortos para TikTok/Reels',
        'Crea carruseles con los puntos más importantes',
      ],
    },
  ];

  workflows.forEach(function (w) {
    html += '<div class="strategy-card">'
      + '<h5>' + w.title + '</h5>'
      + '<p>' + w.desc + '</p>'
      + '<ul style="margin-top:.5rem">'
      + w.steps.map(function (s) { return '<li>' + s + '</li>'; }).join('')
      + '</ul></div>';
  });
  html += '</div>';

  html += '<div class="strategy-section"><h4>🛠️ Stack de Herramientas de Automatización</h4>';
  AUTOMATION_TOOLS.forEach(function (t) {
    html += '<div class="strategy-card">'
      + '<h5>' + t.icon + ' ' + t.name + '</h5>'
      + '<div style="margin-bottom:.4rem"><span class="tag teal">' + t.category + '</span></div>'
      + '<p>' + t.description + '</p>'
      + '</div>';
  });
  html += '</div>';

  html += '<div class="strategy-section">'
    + '<h4>🤖 Automatización con IA para Creación de Contenido</h4>'
    + '<div class="strategy-card"><h5>Prompts esenciales para tu estrategia</h5><ul>'
    + '<li>Generación de ideas de contenido semanales basadas en tendencias</li>'
    + '<li>Redacción de captions adaptados a cada plataforma y tono de marca</li>'
    + '<li>Creación de scripts para videos cortos y reels</li>'
    + '<li>Respuestas a comentarios y mensajes directos</li>'
    + '<li>Análisis de métricas y sugerencias de optimización</li>'
    + '<li>Generación de newsletters semanales</li>'
    + '</ul></div>'
    + '</div>';

  return html;
}

// ── Calendar Tab ───────────────────────────────────────────────────────

function buildCalendar() {
  const weekDays = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];

  let grid = '<div class="calendar-grid">';
  weekDays.forEach(function (d) {
    grid += '<div class="calendar-day header">' + d + '</div>';
  });
  CALENDAR_ITEMS.forEach(function (item) {
    grid += '<div class="calendar-day has-content">'
      + '<div>' + item.emoji + '</div>'
      + '<div style="font-size:.65rem;color:var(--primary-light);margin-top:.2rem">' + item.type + '</div>'
      + '<div class="content-label">' + item.platform + '</div>'
      + '</div>';
  });
  grid += '</div>';

  const freqRows = [
    ['Instagram Feed',   '4–5× / semana',  '9 am, 12 pm, 6 pm'],
    ['Instagram Reels',  '3–4× / semana',  '9 am, 12 pm, 7 pm'],
    ['TikTok',           '1–3× / día',     '7 am, 12 pm, 7 pm'],
    ['LinkedIn',         '3–5× / semana',  '8 am, 12 pm, 5 pm'],
    ['YouTube',          '1–2× / semana',  'Sáb/Dom 10 am'],
    ['Email Newsletter', '1–2× / semana',  'Mar/Jue 9 am'],
  ];

  const tableRows = freqRows.map(function (r, i) {
    const border = i < freqRows.length - 1 ? 'border-bottom:1px solid var(--border)' : '';
    return '<tr>'
      + '<td style="padding:.6rem;color:var(--text-muted);' + border + '">' + r[0] + '</td>'
      + '<td style="padding:.6rem;color:var(--text-muted);' + border + '">' + r[1] + '</td>'
      + '<td style="padding:.6rem;color:var(--text-muted);' + border + '">' + r[2] + '</td>'
      + '</tr>';
  }).join('');

  const freqTable = '<div class="strategy-section" style="margin-top:1.5rem">'
    + '<h4>📋 Frecuencia de Publicación por Plataforma</h4>'
    + '<div class="strategy-card">'
    + '<table style="width:100%;font-size:.85rem;border-collapse:collapse"><thead>'
    + '<tr style="background:var(--primary-dark)">'
    + '<th style="padding:.6rem;text-align:left;color:#fff">Plataforma</th>'
    + '<th style="padding:.6rem;text-align:left;color:#fff">Frecuencia</th>'
    + '<th style="padding:.6rem;text-align:left;color:#fff">Mejor horario</th>'
    + '</tr></thead><tbody>' + tableRows + '</tbody></table>'
    + '</div></div>';

  return '<div class="strategy-section"><h4>📅 Plantilla de Calendario Editorial (2 semanas)</h4></div>'
    + grid + freqTable;
}

// ── KPIs Tab ───────────────────────────────────────────────────────────

function buildKPIs() {
  const rows = KPI_ROWS.map(function (r) {
    return '<tr>'
      + '<td>' + r[0] + '</td>'
      + '<td>' + r[1] + '</td>'
      + '<td>' + r[2] + '</td>'
      + '<td>' + r[3] + '</td>'
      + '</tr>';
  }).join('');

  const table = '<div class="strategy-section">'
    + '<h4>📈 KPIs por Bloque del Business Model Canvas</h4>'
    + '<div class="strategy-card">'
    + '<table class="kpi-table"><thead><tr>'
    + '<th>Bloque</th><th>KPI Principal</th><th>Herramienta</th><th>Meta sugerida</th>'
    + '</tr></thead><tbody>' + rows + '</tbody></table>'
    + '</div></div>';

  const metrics = '<div class="strategy-section">'
    + '<h4>🎯 Métricas de Contenido Digital</h4>'
    + [
      ['Alcance e Impresiones', [
        'Crecimiento de seguidores (meta: +10 % mensual)',
        'Alcance orgánico por publicación',
        'Impresiones totales por canal',
      ]],
      ['Engagement', [
        'Tasa de engagement (likes + comentarios + shares ÷ seguidores)',
        'Saves y compartidos — indicador de contenido de alto valor',
        'Clics en enlaces (CTR)',
      ]],
      ['Conversión', [
        'Leads generados por canal',
        'Tasa de apertura de emails (meta: > 25 %)',
        'Tasa de conversión de landing pages (meta: > 3 %)',
        'Ventas atribuidas a contenido orgánico',
      ]],
    ].map(function (item) {
      return '<div class="strategy-card"><h5>' + item[0] + '</h5><ul>'
        + item[1].map(function (li) { return '<li>' + li + '</li>'; }).join('')
        + '</ul></div>';
    }).join('')
    + '</div>';

  return table + metrics;
}

// ── Public API ─────────────────────────────────────────────────────────

function generateStrategy() {
  const data = getCanvasData();
  const filled = Object.values(data).some(function (v) { return v.length > 0; });

  if (!filled) {
    alert('Por favor, completa al menos uno de los bloques del Business Model Canvas para generar tu estrategia.');
    return;
  }

  document.getElementById('contentStrategy').innerHTML    = buildContentStrategy(data);
  document.getElementById('automationStrategy').innerHTML = buildAutomation();
  document.getElementById('calendarStrategy').innerHTML   = buildCalendar();
  document.getElementById('kpisStrategy').innerHTML       = buildKPIs();

  const output = document.getElementById('strategyOutput');
  output.style.display = 'block';
  output.scrollIntoView({ behavior: 'smooth' });

  // Reset to first tab
  document.querySelectorAll('.tab-btn').forEach(function (btn) {
    btn.classList.toggle('active', btn.dataset.tab === 'content');
  });
  document.querySelectorAll('.tab-content').forEach(function (el) {
    el.classList.toggle('active', el.id === 'content-tab');
  });
}

function showTab(event, tabName) {
  document.querySelectorAll('.tab-btn').forEach(function (btn) {
    btn.classList.remove('active');
  });
  event.currentTarget.classList.add('active');

  document.querySelectorAll('.tab-content').forEach(function (el) {
    el.classList.remove('active');
  });
  document.getElementById(tabName + '-tab').classList.add('active');
}
