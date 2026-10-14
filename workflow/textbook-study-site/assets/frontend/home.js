(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const escape = value => String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const isLanguage = value => value === 'zh' || value === 'en';
  const requestedLanguage = new URLSearchParams(location.search).get('lang');
  // A URL choice is explicit. A fresh visit always starts in English.
  let language = isLanguage(requestedLanguage) ? requestedLanguage : 'en';
  const t = (zh,en) => language === 'en' ? en : zh;
  const localized = record => language === 'en' ? {...record,...record.en} : record;
  let sourceData;

  const translations = {
    zh: {skip:'跳到课程目录',brand:'学习主页',welcome:'从这里开始。',intro:'选择章节，按知识点学习、练习，并查看分步解析。',contents:'课程目录',footer:'中英文学习笔记',empty:'暂时没有可用章节。',announcement:'已切换为中文。'},
    en: {skip:'Skip to study contents',brand:'STUDY HOME',welcome:'Start here.',intro:'Choose a section to study key concepts, practise, and follow step-by-step solutions.',contents:'Study contents',footer:'Bilingual study notes',empty:'No sections are available yet.',announcement:'Switched to English.'}
  };
  function lessonUrl(section) {
    // The builder validates slugs; retain a runtime check before constructing links.
    if(!/^[a-zA-Z0-9][a-zA-Z0-9_-]*$/.test(section.slug || ''))throw new Error('Invalid section slug.');
    const destination = new URL(location.protocol === 'file:' ? `sections/${section.slug}/index.html` : `sections/${section.slug}/`,location.href);
    destination.searchParams.set('lang',language);
    return destination.href;
  }
  function countLabel(counts) {
    const units = [
      ['concepts','个知识点','concept','concepts'],
      ['examples','道例题','example','examples'],
      ['practice','道配套练习','practice problem','practice problems'],
      ['exercises','道节后习题','exercise','exercises']
    ];
    return units.filter(([key]) => Number.isInteger(counts?.[key]) && counts[key] >= 0 && !(key === 'practice' && counts[key] === 0)).map(([key,zh,singular,plural]) => `${counts[key]} ${t(zh,counts[key] === 1 ? singular : plural)}`).join(' · ');
  }
  function lessonCard(base,index) {
    const section = localized(base);
    const label = section.section ? t(`第 ${section.section} 节`,`Section ${section.section}`) : t('学习单元','Study unit');
    return `<article class="lesson-card" aria-labelledby="lesson-title-${index}"><div class="section-number" aria-hidden="true">${escape(section.section || index + 1)}</div><div class="lesson-content"><p class="lesson-label">${escape(label)}</p><h4 id="lesson-title-${index}">${escape(section.title)}</h4><p class="lesson-meta">${escape(countLabel(base.counts))}</p><a class="lesson-link" href="${escape(lessonUrl(base))}"><span>${escape(t(`开始学习 ${section.section || ''}`,`Study ${section.section || 'this section'}`))}</span><span aria-hidden="true">→</span></a></div></article>`;
  }
  function renderSections() {
    const sections = sourceData.sections;
    const groups = [];
    sections.forEach((base,index) => {
      const section = localized(base);
      const chapter = typeof section.chapter === 'string' ? section.chapter : '';
      // Group adjacent sections only, preserving the supplied textbook order.
      let group = groups[groups.length - 1];
      if(!group || group.chapter !== chapter){group={chapter,items:[]};groups.push(group);}
      group.items.push({base,index});
    });
    $('#course-contents').innerHTML = groups.map(group => `<div class="course-section-group">${group.chapter ? `<div class="chapter-heading"><p class="chapter-label">${t('章节','CHAPTER')}</p><h3>${escape(group.chapter)}</h3></div>` : ''}${group.items.map(({base,index}) => lessonCard(base,index)).join('')}</div>`).join('');
    $('#home-empty').hidden = sections.length !== 0;
  }
  function render() {
    const text = translations[language];
    const course = localized(sourceData.course);
    const title = String(course.title || t('课程','Course'));
    document.documentElement.lang = language === 'en' ? 'en' : 'zh-Hans';
    document.title = `${title} · ${t('学习主页','Study home')}`;
    $('meta[name="description"]').content = t(`${title} 中英文学习目录：知识点、例题、练习与分步解析。`,`${title} bilingual study contents: concepts, examples, practice, and step-by-step solutions.`);
    $$('[data-i18n]').forEach(element => { element.textContent = text[element.dataset.i18n]; });
    $$('.course-title,.brand-title').forEach(element => { element.textContent = title; });
    $$('[data-language]').forEach(button => { const active = button.dataset.language === language;button.classList.toggle('is-active',active);button.setAttribute('aria-pressed',String(active)); });
    const home = new URL(location.protocol === 'file:' ? 'index.html' : './',location.href);
    home.searchParams.set('lang',language);
    $('#home-link').href = home.href;
    $('#home-link').setAttribute('aria-label',t('课程首页','Course home'));
    renderSections();
  }
  function start() {
    const inline = $('#course-data');
    sourceData = window.COURSE_DATA || JSON.parse(inline.textContent);
    if(!sourceData.course || !Array.isArray(sourceData.sections))throw new Error('Expected course and sections data.');
    $$('[data-language]').forEach(button => button.addEventListener('click',() => {
      const next = button.dataset.language;
      if(!isLanguage(next) || next === language)return;
      language = next;
      const current = new URL(location.href);
      current.searchParams.set('lang',language);
      try {history.replaceState(null,'',current.href);} catch (_) {}
      render();
      $('#announcement').textContent = translations[language].announcement;
    }));
    render();
  }
  try {start();} catch(error) {$('#home-error').hidden=false;$('#home-error').textContent=t('课程目录暂时无法载入，请核对内容文件。','Study contents could not be loaded. Check the content files.');console.error(error);}
})();
