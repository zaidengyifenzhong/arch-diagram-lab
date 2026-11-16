"use strict";

function matchesFilters(item, filters) {
  const query = filters.query.trim().toLocaleLowerCase();
  const haystack = [item.figure_title, item.figure_type || "", item.paper_title, item.paper_short || "", item.category, item.attribution, item.object_group || "", item.specific_object || ""].join(" ").toLocaleLowerCase();
  return (!filters.object || item.object_group === filters.object) &&
    (!filters.paper || item.paper_id === filters.paper || item.paper_title === filters.paper) &&
    (!filters.category || item.category === filters.category) &&
    (!filters.type || item.figure_type === filters.type) &&
    (!filters.license || item.license_name === filters.license) &&
    (!query || haystack.includes(query));
}

function uniqueValues(items, key) {
  return [...new Set(items.map(item => item[key]))].sort((a, b) => a.localeCompare(b));
}

function resolveFigureReference(items, paperId, figureId) {
  if (!/^F[1-9][0-9]*$/.test(figureId)) return undefined;
  return items.find(item => item.paper_id === paperId && item.figure_number === Number(figureId.slice(1)));
}

function prepareItems(data) {
  const objects = new Map((data.paper_objects || []).map(p => [p.paper_id, p]));
  return data.items.map(item => ({...item,
    object_group: objects.get(item.paper_id)?.object_group || "",
    specific_object: objects.get(item.paper_id)?.specific_object || ""}));
}

if (typeof module !== "undefined") module.exports = { matchesFilters, uniqueValues, resolveFigureReference, prepareItems };

if (typeof document !== "undefined") {
  const data = JSON.parse(document.getElementById("gallery-data").textContent);
  const items = prepareItems(data);
  const gallery = document.getElementById("gallery");
  const search = document.getElementById("search");
  const paper = document.getElementById("paper");
  const object = document.getElementById("research-object");
  const category = document.getElementById("category");
  const license = document.getElementById("license");
  const figureType = document.getElementById("figure-type");
  const empty = document.getElementById("empty");
  const viewer = document.getElementById("viewer");
  const readingPath = document.getElementById("reading-path");
  let shownGuidePaper = null;
  let lastTrigger = null;
  const el = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text) element.textContent = text;
    return element;
  };
  const link = (label, url) => {
    const a = el("a", "", label);
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    return a;
  };

  const paperGroups = new Map();
  for (const item of items) {
    const key = item.paper_id || item.paper_title;
    if (!paperGroups.has(key)) paperGroups.set(key, {label: item.paper_short || item.paper_title, count:0, notice:item.paper_notice || "", object:item.object_group || ""});
    paperGroups.get(key).count += 1;
  }
  for (const value of uniqueValues(items, "object_group").filter(Boolean)) {
    const option = el("option", "", value);
    option.value = value;
    object.append(option);
  }
  object.closest("label").hidden = !data.paper_objects?.length;
  for (const [key, group] of paperGroups) {
    const option = el("option", "", `${group.label} (${group.count})${group.notice ? " · 附说明" : ""}`);
    option.value = key;
    paper.append(option);
  }
  for (const [select, key] of [[category, "category"], [figureType, "figure_type"], [license, "license_name"]]) {
    for (const value of uniqueValues(items, key)) {
      const option = el("option", "", value);
      option.value = value;
      select.append(option);
    }
  }

  function openFigure(item, trigger) {
    lastTrigger = trigger;
    const img = document.getElementById("viewer-img");
    img.src = item.asset;
    img.alt = item.alt_text;
    document.getElementById("viewer-title").textContent = `${item.figure_title} · ${item.figure_type} · PDF 第 ${item.pdf_page} 页`;
    document.getElementById("viewer-paper").textContent = item.paper_title;
    document.getElementById("viewer-attribution").textContent = `${item.attribution} · ${item.license_name} · ${item.modifications} · ${item.reuse_notice || ""}`;
    document.getElementById("viewer-source").href = item.source_url;
    document.getElementById("viewer-source-page").href = item.source_page_url || item.source_url;
    const note = document.getElementById("viewer-note");
    note.textContent = item.source_note || "";
    note.hidden = !item.source_note;
    document.getElementById("viewer-original").href = item.asset;
    viewer.showModal();
  }

  function render() {
    const filtered = items.filter(item => matchesFilters(item, { query: search.value, paper: paper.value, object: object.value, category: category.value, type: figureType.value, license: license.value }));
    const fragment = document.createDocumentFragment();
    for (const item of filtered) {
      const card = el("article", "card");
      card.id = `figure-${item.id}`;
      card.tabIndex = -1;
      const button = el("button", "image-button");
      button.type = "button";
      button.setAttribute("aria-label", `查看大图：${item.figure_title}，${item.figure_type}`);
      const img = el("img");
      img.src = item.asset;
      img.alt = item.alt_text;
      img.width = item.width;
      img.height = item.height;
      img.loading = "lazy";
      img.decoding = "async";
      button.append(img, el("span", "expand", "查看大图 ↗"));
      button.addEventListener("click", () => openFigure(item, button));
      const body = el("div", "card-body");
      const pageLink = link(`PDF 第 ${item.pdf_page} 页 ↗`, item.source_page_url || item.source_url);
      pageLink.className = "page-reference";
      body.append(el("p", "paper", item.paper_title), el("h2", "", `${item.figure_title} · ${item.figure_type}`), pageLink, el("p", "category", item.category));
      if (item.specific_object) body.append(el("p", "object-label", item.specific_object));
      if (item.source_note) body.append(el("p", "source-note", item.source_note));
      const provenance = el("details", "provenance");
      provenance.append(el("summary", "", "署名与使用许可"), el("p", "attribution", item.attribution));
      body.append(provenance);
      const links = el("div", "card-links");
      if (item.reuse_notice) provenance.append(el("p", "license-warning", item.reuse_notice));
      links.append(link("论文来源 ↗", item.source_url), link(item.license_name, item.license_url));
      body.append(links);
      card.append(button, body);
      fragment.append(card);
    }
    gallery.replaceChildren(fragment);
    empty.hidden = filtered.length !== 0;
    if (items.length === 0) {
      empty.querySelector("h2").textContent = "原图准备中";
      empty.querySelector("p").textContent = "当前本地草稿尚未加入原图。";
    }
    document.getElementById("result-count").textContent = `显示 ${filtered.length} / ${items.length} 张原图`;
    const paperNotice = document.getElementById("paper-notice");
    const selectedGroup = paperGroups.get(paper.value);
    paperNotice.textContent = selectedGroup?.notice || "";
    paperNotice.hidden = !selectedGroup?.notice;
    renderReadingGuide();
  }

  function renderReadingGuide() {
    if (shownGuidePaper === paper.value) return;
    shownGuidePaper = paper.value;
    const guide = (data.reading_guides || []).find(g => g.paper_id === paper.value);
    readingPath.replaceChildren();
    readingPath.hidden = !guide;
    if (!guide) return;
    const details = el("details", "reading-guide");
    details.append(el("summary", "", "阅读建议，并非每篇必备清单"));
    const body = el("div", "reading-body");
    body.append(el("p", "reading-object", `研究对象：${guide.primary_object} · ${guide.specific_object}`));
    body.append(el("p", "", guide.conditional_design_advice));
    body.append(el("p", "", `本篇阅读路径：${guide.this_paper_figure_sequence}`));
    const jumps = el("div", "figure-jumps");
    for (const example of guide.source_examples) {
      const item = resolveFigureReference(items, guide.paper_id, example.figure_id);
      const a = el("a", "", `图 ${item.figure_number} · p.${item.pdf_page}`);
      a.href = `#figure-${item.id}`;
      a.addEventListener("click", event => {
        event.preventDefault();
        search.value = category.value = figureType.value = license.value = "";
        render();
        const target = document.getElementById(`figure-${item.id}`);
        target.scrollIntoView({block:"center"});
        target.focus({preventScroll:true});
      });
      jumps.append(a);
    }
    body.append(jumps, el("p", "source-note", guide.source_ambiguity_or_scope));
    details.append(body);
    readingPath.append(details);
  }

  search.addEventListener("input", render);
  paper.addEventListener("change", render);
  object.addEventListener("change", () => {
    for (const option of paper.options) {
      option.hidden = Boolean(option.value && object.value && paperGroups.get(option.value)?.object !== object.value);
    }
    if (paper.value && object.value && paperGroups.get(paper.value)?.object !== object.value) paper.value = "";
    render();
  });
  license.addEventListener("change", render);
  category.addEventListener("change", render);
  figureType.addEventListener("change", render);
  document.getElementById("reset").addEventListener("click", () => {
    search.value = paper.value = object.value = category.value = figureType.value = license.value = "";
    for (const option of paper.options) option.hidden = false;
    render();
    search.focus();
  });
  document.getElementById("close").addEventListener("click", () => viewer.close());
  viewer.addEventListener("click", event => {
    const bounds = viewer.getBoundingClientRect();
    if (event.target === viewer && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) viewer.close();
  });
  viewer.addEventListener("close", () => {
    document.getElementById("viewer-img").removeAttribute("src");
    if (lastTrigger?.isConnected) lastTrigger.focus();
  });
  render();
}
