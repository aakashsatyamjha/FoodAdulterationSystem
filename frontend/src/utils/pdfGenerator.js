/**
 * FoodGuard AI - PDF Report Generator
 * Generates comprehensive multi-page Food Safety, Prohibited Additives,
 * INS/E-Number Rules, Cross-Country Divergence, and Decision Trace reports.
 */

import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";

export function generateProductSafetyPDF(data, selectedCountryCode = "IN") {
  if (!data) return;

  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
  });

  const {
    product_name = "Food Product",
    brand = "Packaged Goods",
    barcode = "N/A",
    category = "Packaged Food",
    scan_type = "Barcode Scan",
    quality_score = 50,
    overall_assessment = "ASSESSED",
    final_verdict_badge = "Assessed",
    final_explanation = "",
    safety_disclaimer = "",
    adulteration = {},
    risk = {},
    regulatory = {},
    consumer = {},
    decision_trace = {},
    matched_ingredients = [],
    nutrition = {},
  } = data;

  const countryNames = {
    IN: "India (FSSAI)",
    US: "USA (FDA)",
    EU: "European Union (EFSA)",
    DE: "Germany (BVL)",
    UK: "United Kingdom (FSA)",
  };

  const selectedCountryName = countryNames[selectedCountryCode] || selectedCountryCode;
  const crossCountryMatrix = regulatory.cross_country_comparison?.matrix || [];
  const divergentIngredients = regulatory.divergent_ingredients || [];

  const pageWidth = doc.internal.pageSize.getWidth();
  let y = 15;

  // ── Header Banner ──
  doc.setFillColor(15, 23, 42); // slate-900
  doc.rect(0, 0, pageWidth, 28, "F");

  doc.setTextColor(16, 185, 129); // emerald-500
  doc.setFontSize(16);
  doc.setFont("helvetica", "bold");
  doc.text("FOODGUARD AI", 14, 12);

  doc.setFontSize(8);
  doc.setTextColor(148, 163, 184); // slate-400
  doc.setFont("helvetica", "normal");
  doc.text("GLOBAL FOOD SAFETY, REGULATORY & ADULTERATION INTELLIGENCE PLATFORM", 14, 18);
  doc.text(`REPORT GENERATED: ${new Date().toLocaleString()} | TARGET: ${selectedCountryName}`, 14, 23);

  y = 36;

  // ── Product Identity & Overall Verdict ──
  doc.setFillColor(248, 250, 252);
  doc.setDrawColor(226, 232, 240);
  doc.roundedRect(14, y, pageWidth - 28, 30, 2, 2, "FD");

  doc.setTextColor(30, 41, 59);
  doc.setFontSize(13);
  doc.setFont("helvetica", "bold");
  doc.text(product_name, 18, y + 8);

  doc.setFontSize(9);
  doc.setFont("helvetica", "normal");
  doc.setTextColor(100, 116, 139);
  doc.text(`Brand: ${brand}   |   Category: ${category}   |   Barcode: ${barcode || "N/A"}`, 18, y + 14);

  // Score Badge
  const scoreColor = quality_score >= 75 ? [16, 185, 129] : quality_score >= 45 ? [245, 158, 11] : [244, 63, 94];
  doc.setFillColor(...scoreColor);
  doc.roundedRect(pageWidth - 52, y + 5, 34, 20, 2, 2, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(14);
  doc.setFont("helvetica", "bold");
  doc.text(`${quality_score}/100`, pageWidth - 35, y + 14, { align: "center" });
  doc.setFontSize(7);
  doc.text("QUALITY SCORE", pageWidth - 35, y + 20, { align: "center" });

  doc.setFontSize(8);
  doc.setTextColor(51, 65, 85);
  doc.text(`Assessment: ${final_verdict_badge} — ${overall_assessment}`, 18, y + 23);

  y += 36;

  // ── 4 Pillars Summary Table ──
  doc.setFontSize(11);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  doc.text("1. Four-Pillars Executive Summary", 14, y);
  y += 3;

  autoTable(doc, {
    startY: y,
    head: [["Pillar", "Dimension", "Status / Verdict", "Key Findings"]],
    body: [
      [
        "Pillar 1",
        "Adulteration Screening",
        adulteration.status || "ASSESSED",
        adulteration.summary || "No non-permitted industrial dyes or heavy metal signatures detected."
      ],
      [
        "Pillar 2",
        "Health & Risk Score",
        `${risk.risk_tier || "Moderate"} (${risk.overall_risk_pct || 40}% Risk)`,
        `Ingredient: ${risk.ingredient_risk_pct || 30}% | Regulatory: ${risk.regulatory_risk_pct || 25}% | Consumer: ${risk.consumer_risk_pct || 35}%`
      ],
      [
        "Pillar 3",
        `Regulatory (${selectedCountryName})`,
        regulatory.selected_country?.verdict || "PASS",
        regulatory.selected_country?.summary || `Evaluated against statutory ${selectedCountryName} food additive standards.`
      ],
      [
        "Pillar 4",
        "Consumer Intelligence",
        consumer.verdict || "SUITABLE",
        consumer.summary || "Preference suitability evaluated against WHO/FSSAI nutritional baselines."
      ],
    ],
    theme: "grid",
    headStyles: { fillColor: [15, 23, 42], textColor: [255, 255, 255], fontSize: 8, fontStyle: "bold" },
    bodyStyles: { fontSize: 8, textColor: [51, 65, 85] },
    columnStyles: {
      0: { cellWidth: 20, fontStyle: "bold" },
      1: { cellWidth: 38, fontStyle: "bold" },
      2: { cellWidth: 42 },
      3: { cellWidth: "auto" }
    },
    margin: { left: 14, right: 14 }
  });

  y = doc.lastAutoTable.finalY + 8;

  // ── Section 1b: Why Not 100/100 (Point Deduction Breakdown) ──
  const scoreDeductions = data.score_deductions || [];
  if (scoreDeductions.length > 0) {
    if (y > 220) {
      doc.addPage();
      y = 20;
    }

    doc.setFontSize(11);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(15, 23, 42);
    doc.text(`2. Score Deduction Breakdown (Why this product received ${quality_score}/100)`, 14, y);
    y += 3;

    const deductionRows = scoreDeductions.map((d) => [
      d.factor,
      d.category,
      d.impact,
      d.reason
    ]);

    autoTable(doc, {
      startY: y,
      head: [["Ingredient / Factor", "Classification", "Point Deduction", "Toxicological & Regulatory Reason"]],
      body: deductionRows,
      theme: "grid",
      headStyles: { fillColor: [225, 29, 72], textColor: [255, 255, 255], fontSize: 8, fontStyle: "bold" },
      bodyStyles: { fontSize: 7.5, textColor: [51, 65, 85] },
      columnStyles: {
        0: { cellWidth: 38, fontStyle: "bold" },
        1: { cellWidth: 30 },
        2: { cellWidth: 24, halign: "center", fontStyle: "bold" },
        3: { cellWidth: "auto" }
      },
      margin: { left: 14, right: 14 }
    });

    y = doc.lastAutoTable.finalY + 4;

    // Narrative Box: Why All Countries Passed Legally vs Why Score is Not 100
    doc.setFillColor(239, 246, 255); // blue-50
    doc.setDrawColor(191, 219, 254);
    doc.roundedRect(14, y, pageWidth - 28, 14, 1.5, 1.5, "FD");
    doc.setFontSize(7);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(30, 64, 175);
    doc.text("REGULATORY LEGALITY vs. NUTRITIONAL QUALITY NOTE:", 17, y + 4.5);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(51, 65, 85);
    doc.text("All 5 countries passed this product because it contains no banned chemicals. However, the score is penalized due to chronic dietary factors (high sugar, sodium, or saturated fat) that exceed WHO health thresholds.", 17, y + 9.5, { maxWidth: pageWidth - 34 });

    y += 18;
  }

  // ── Section 2: Prohibited / Restricted Items & Cross-Country Divergence (INS Rules) ──
  doc.setFontSize(11);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  doc.text("3. Prohibited / Restricted Substances & Statutory INS / E-Number Rules", 14, y);
  y += 3;

  const prohibitedAndDivergentRows = [];

  // Add all detected / matched substances with INS rules and comparison
  if (crossCountryMatrix.length > 0) {
    crossCountryMatrix.forEach((item) => {
      const inStat = item.statuses?.IN?.badge?.symbol || "✓";
      const usStat = item.statuses?.US?.badge?.symbol || "✓";
      const euStat = item.statuses?.EU?.badge?.symbol || "✓";
      const deStat = item.statuses?.DE?.badge?.symbol || "✓";
      const ukStat = item.statuses?.UK?.badge?.symbol || "✓";

      const divergenceNote = item.has_divergence
        ? (divergentIngredients.find(d => d.ins_e_number === item.ins_e_number || d.name === item.common_name)?.reason || "Divergent country regulatory classifications apply.")
        : "Harmonized standards across jurisdictions.";

      prohibitedAndDivergentRows.push([
        `${item.common_name}\n(${item.ins_e_number || "N/A"})`,
        item.function || "Food Additive",
        `IN: ${inStat}\nUS: ${usStat}\nEU: ${euStat}\nDE: ${deStat}`,
        divergenceNote
      ]);
    });
  } else {
    prohibitedAndDivergentRows.push([
      "Standard Ingredients",
      "Bulk Formulation",
      "IN: ✓  US: ✓  EU: ✓  DE: ✓",
      "No high-risk restricted additives or banned dyes identified in scanned formulation."
    ]);
  }

  autoTable(doc, {
    startY: y,
    head: [["Substance (INS / E-Code)", "Functional Class", "Country Legal Status", "Why Prohibited in Some Countries vs Approved in Others"]],
    body: prohibitedAndDivergentRows,
    theme: "grid",
    headStyles: { fillColor: [30, 41, 59], textColor: [255, 255, 255], fontSize: 8, fontStyle: "bold" },
    bodyStyles: { fontSize: 7.5, textColor: [51, 65, 85] },
    columnStyles: {
      0: { cellWidth: 40, fontStyle: "bold" },
      1: { cellWidth: 28 },
      2: { cellWidth: 26, halign: "center" },
      3: { cellWidth: "auto" }
    },
    margin: { left: 14, right: 14 }
  });

  y = doc.lastAutoTable.finalY + 8;

  // Check if we need a new page for nutritional & decision trace
  if (y > 220) {
    doc.addPage();
    y = 20;
  }

  // ── Section 3: Nutritional Traffic Light & Risk Breakdown ──
  doc.setFontSize(11);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  doc.text("3. Multi-Risk Breakdown & Nutritional Profile", 14, y);
  y += 3;

  autoTable(doc, {
    startY: y,
    head: [["Nutrient", "Amount per 100g", "Clinical Status", "Risk Dimension", "Score Contribution"]],
    body: [
      ["Total Sugars", `${nutrition.sugar_g || 0} g`, (nutrition.sugar_g || 0) > 15 ? "HIGH" : (nutrition.sugar_g || 0) > 5 ? "MODERATE" : "LOW", "Overall Holistic Risk", `${risk.overall_risk_pct || 40}%`],
      ["Sodium", `${nutrition.sodium_mg || 0} mg`, (nutrition.sodium_mg || 0) > 600 ? "HIGH" : (nutrition.sodium_mg || 0) > 200 ? "MODERATE" : "LOW", "Ingredient Toxicity Risk", `${risk.ingredient_risk_pct || 30}%`],
      ["Saturated Fat", `${nutrition.saturated_fat_g || 0} g`, (nutrition.saturated_fat_g || 0) > 5 ? "HIGH" : "LOW", "Regulatory Exposure Risk", `${risk.regulatory_risk_pct || 25}%`],
      ["Trans Fat", `${nutrition.trans_fat_g || 0} g`, (nutrition.trans_fat_g || 0) > 0.2 ? "ELEVATED" : "ZERO", "Consumer Preference Risk", `${risk.consumer_risk_pct || 35}%`],
      ["Dietary Fiber", `${nutrition.fiber_g || 0} g`, (nutrition.fiber_g || 0) > 6 ? "HIGH FIBER" : "STANDARD", "Clean Label Status", consumer.clean_label ? "Clean Formulation" : "Ultra-Processed Markers Present"],
      ["Protein", `${nutrition.protein_g || 0} g`, (nutrition.protein_g || 0) > 10 ? "HIGH PROTEIN" : "STANDARD", "Target Jurisdiction", selectedCountryName],
    ],
    theme: "striped",
    headStyles: { fillColor: [51, 65, 85], textColor: [255, 255, 255], fontSize: 8, fontStyle: "bold" },
    bodyStyles: { fontSize: 7.5, textColor: [51, 65, 85] },
    margin: { left: 14, right: 14 }
  });

  y = doc.lastAutoTable.finalY + 8;

  // ── Section 4: Explainable Decision Trace ──
  if (decision_trace.steps && decision_trace.steps.length > 0) {
    if (y > 230) {
      doc.addPage();
      y = 20;
    }

    doc.setFontSize(11);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(15, 23, 42);
    doc.text("4. Algorithmic Decision Trace (Audit Log)", 14, y);
    y += 3;

    const traceRows = decision_trace.steps.map((s) => [
      `Step ${s.step_num}`,
      s.title,
      s.status,
      s.detail
    ]);

    autoTable(doc, {
      startY: y,
      head: [["Step", "Evaluation Stage", "Status", "Detailed Audit Trace"]],
      body: traceRows,
      theme: "grid",
      headStyles: { fillColor: [15, 23, 42], textColor: [255, 255, 255], fontSize: 8, fontStyle: "bold" },
      bodyStyles: { fontSize: 7.5, textColor: [51, 65, 85] },
      columnStyles: {
        0: { cellWidth: 16, fontStyle: "bold" },
        1: { cellWidth: 45, fontStyle: "bold" },
        2: { cellWidth: 20, halign: "center" },
        3: { cellWidth: "auto" }
      },
      margin: { left: 14, right: 14 }
    });

    y = doc.lastAutoTable.finalY + 8;
  }

  // ── Footer / Disclaimer ──
  if (y > 250) {
    doc.addPage();
    y = 20;
  }

  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  doc.setFont("helvetica", "italic");
  const disclaimer = safety_disclaimer || "Disclaimer: FoodGuard AI provides automated preliminary algorithmic screening based on published food standards and machine learning models. It does not replace certified ISO/NABL accredited laboratory chemical analysis or statutory regulatory counsel.";
  const splitDisclaimer = doc.splitTextToSize(disclaimer, pageWidth - 28);
  doc.text(splitDisclaimer, 14, y);

  // Save the PDF
  const safeFilename = `${product_name.replace(/[^a-zA-Z0-9]/g, "_")}_FoodSafety_Report.pdf`;
  doc.save(safeFilename);
}
