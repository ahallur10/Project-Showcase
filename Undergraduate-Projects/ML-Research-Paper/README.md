<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Music Genre Classification (GTZAN) — Course Project</title>
<style>
  :root { --fg:#0b1220; --muted:#5b687a; --bg:#ffffff; --card:#f7f9fc; --accent:#3b82f6; }
  html,body { margin:0; padding:0; background:var(--bg); color:var(--fg); font:16px/1.6 system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, "Noto Sans"; }
  .wrap { max-width: 900px; margin: 2.5rem auto; padding: 0 1.2rem; }
  h1,h2,h3 { line-height:1.25; margin: 1.6rem 0 .8rem; }
  h1 { font-size:2rem; }
  h2 { font-size:1.45rem; border-bottom:1px solid #e6ebf2; padding-bottom:.4rem; }
  h3 { font-size:1.1rem; }
  p, li { color:#0f172a; }
  .muted { color:var(--muted); }
  .pill { display:inline-block; padding:.2rem .6rem; border-radius:999px; background:#eef2ff; color:#3730a3; font-size:.8rem; margin-right:.4rem; }
  .card { background:var(--card); border:1px solid #e6ebf2; border-radius:12px; padding:1rem 1.1rem; margin:1rem 0; }
  pre { background:#0b1020; color:#f1f5f9; padding:1rem; border-radius:10px; overflow:auto; line-height:1.45; }
  code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
  table { width:100%; border-collapse: collapse; margin: .6rem 0 1.2rem; }
  th, td { border:1px solid #e6ebf2; padding:.6rem .5rem; text-align:left; }
  th { background:#f3f6fb; }
</style>
</head>
<body>
<main class="wrap">
  <header>
    <h1>Music Genre Classification (GTZAN) — Course Project</h1>
    <p><em>Classical ML baseline with feature selection. Original course submission (kept intact) + notes on suggested improvements.</em></p>
    <div>
      <span class="pill">R</span>
      <span class="pill">GTZAN</span>
      <span class="pill">MFCC</span>
      <span class="pill">Chroma</span>
      <span class="pill">Logistic Regression</span>
      <span class="pill">Random Forest</span>
      <span class="pill">kNN</span>
    </div>
  </header>

  <section>
    <h2>Overview</h2>
    <p>
      This project explores music genre classification on the GTZAN dataset using classical machine-learning models.
      The focus is on feature engineering (MFCC &amp; Chroma), simple baselines (Logistic Regression, Random Forest, kNN),
      and feature selection (RFE, Boruta).
    </p>
    <p><strong>Status:</strong> The repo preserves the <strong>original course code</strong> (graded at 94%). A short <em>Suggested Improvements</em> section documents what I’d fix in a future pass.</p>
  </section>

  <section>
    <h2>Dataset</h2>
    <ul>
      <li><strong>GTZAN:</strong> 10 genres, ~100 clips/genre (30-sec WAV files).</li>
      <li><strong>Access:</strong> Not included in this repo. Download separately and update <code>data_path</code> in the script(s).</li>
      <li><strong>Use:</strong> Research/education only. Please respect the dataset license.</li>
    </ul>
  </section>

  <section>
    <h2>Features</h2>
    <ul>
      <li><strong>Basic:</strong> <code>tempo</code> and <code>spectral_centroid</code> as implemented in the original code.</li>
      <li><strong>Engineered:</strong> MFCC (13 coefficients) and Chroma (12 bins), summarized as <strong>means per track</strong> for compact modeling.</li>
      <li><strong>Selection:</strong> Recursive Feature Elimination (RFE) and Boruta to compare feature utility.</li>
    </ul>
    <div class="card">
      <strong>Heads-up (transparency):</strong> In the original code, <code>tempo</code> returns the audio <em>sample rate</em> (not BPM), and <code>spectral_centroid</code> is approximated via mean FFT magnitude.
      See <a href="#suggested-improvements">Suggested Improvements</a> for how I’d correct this.
    </div>
  </section>

  <section>
    <h2>Models</h2>
    <ul>
      <li><strong>Logistic Regression</strong> (multinomial)</li>
      <li><strong>Random Forest</strong></li>
      <li><strong>k-Nearest Neighbors</strong> (kNN)</li>
    </ul>

    <h3>Example: Training Logistic Regression (original)</h3>
    <pre><code class="language-r">library(caret)
library(nnet)

set.seed(42)
train_index &lt;- createDataPartition(feature_data$genre, p = 0.7, list = FALSE)
train_data  &lt;- feature_data[train_index, ]
test_data   &lt;- feature_data[-train_index, ]

model_logreg &lt;- multinom(genre ~ tempo + spectral_centroid, data = train_data)
pred &lt;- predict(model_logreg, newdata = test_data)
acc  &lt;- mean(pred == test_data$genre)
cat("Accuracy:", acc, "\n")</code></pre>

    <h3>Example: MFCC + Chroma (summary features)</h3>
    <pre><code class="language-r"># After computing MFCC/Chroma vectors per file:
feature_data_summary &lt;- feature_data %&gt;%
  mutate(
    mean_mfcc   = purrr::map_dbl(mfcc, mean),
    mean_chroma = purrr::map_dbl(chroma, mean)
  ) %&gt;%
  select(genre, mean_mfcc, mean_chroma) %&gt;%
  na.omit()

set.seed(42)
idx &lt;- createDataPartition(feature_data_summary$genre, p = 0.8, list = FALSE)
tr  &lt;- feature_data_summary[idx,  ] %&gt;% mutate(genre = as.factor(genre))
te  &lt;- feature_data_summary[-idx, ] %&gt;% mutate(genre = as.factor(genre))

library(randomForest)
m_rf   &lt;- randomForest(genre ~ mean_mfcc + mean_chroma, data = tr, ntree = 50, maxnodes = 10)
predRF &lt;- predict(m_rf, newdata = te)
mean(predRF == te$genre)</code></pre>
  </section>

  <section>
    <h2>Evaluation</h2>
    <ul>
      <li><strong>Splits:</strong> Train/test <strong>70/30</strong> (and <strong>80/20</strong> for MFCC/Chroma summaries).</li>
      <li><strong>Metrics:</strong> Accuracy, per-class <strong>F1</strong>, Confusion Matrix.</li>
      <li><strong>Feature Selection:</strong> RFE (RF estimator) and <strong>Boruta</strong>.</li>
    </ul>
    <p class="muted">Use <code>caret::confusionMatrix</code> for confusion matrices and your plotting code for RFE vs Boruta comparisons.</p>
  </section>

  <section>
    <h2>Results (snapshot)</h2>
    <p class="muted">Replace placeholders if you want, or keep this lightweight for admissions.</p>
    <table>
      <thead>
        <tr><th>Model</th><th>Features</th><th>Accuracy</th><th>Macro F1</th></tr>
      </thead>
      <tbody>
        <tr><td>Logistic Regression</td><td>tempo + spectral_centroid</td><td>~&lt;fill&gt;</td><td>~&lt;fill&gt;</td></tr>
        <tr><td>Random Forest</td><td>tempo + spectral_centroid</td><td>~&lt;fill&gt;</td><td>~&lt;fill&gt;</td></tr>
        <tr><td>kNN</td><td>tempo + spectral_centroid</td><td>~&lt;fill&gt;</td><td>~&lt;fill&gt;</td></tr>
        <tr><td>Random Forest</td><td>mean(MFCC) + mean(Chroma)</td><td>~&lt;fill&gt;</td><td>~&lt;fill&gt;</td></tr>
        <tr><td>kNN</td><td>mean(MFCC) + mean(Chroma)</td><td>~&lt;fill&gt;</td><td>~&lt;fill&gt;</td></tr>
      </tbody>
    </table>
    <div class="card">
      <strong>Takeaways:</strong>
      <ul>
        <li>MFCC + Chroma summaries improved baseline performance across models.</li>
        <li>“Tempo” (as implemented) had limited utility; spectral information mattered more.</li>
        <li>RFE and Boruta highlighted MFCC/Chroma as most informative.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>How to Run (original)</h2>
    <ol>
      <li>Install R packages used in the scripts:
        <code>tidyverse</code>, <code>caret</code>, <code>tuneR</code>, <code>randomForest</code>, <code>kknn</code>, <code>nnet</code>, <code>Boruta</code>, <code>imputeTS</code>, <code>ggplot2</code>, etc.</li>
      <li>Update <code>data_path</code> to your local GTZAN directory in the script.</li>
      <li>Run the script(s) in R/RStudio. Metrics print to console; plots appear in the Viewer.</li>
    </ol>
    <div class="card">
      <strong>Tip:</strong> For reproducibility, consider using <code>{renv}</code> to snapshot package versions.
    </div>
  </section>

  <section id="suggested-improvements">
    <h2>Suggested Improvements (short &amp; honest)</h2>
    <ol>
      <li><strong>Tempo → true BPM:</strong> Replace sample-rate proxy with beat tracking (e.g., <code>librosa.beat.beat_track</code>) or an R equivalent.</li>
      <li><strong>Spectral centroid:</strong> Compute via spectrum properties (e.g., <code>seewave::specprop</code>) instead of mean FFT magnitude.</li>
      <li><strong>MFCC/Chroma shaping:</strong> Spread vectors into <em>columns</em> with <code>tidyr::unnest_wider</code>, then compute summary stats (means).</li>
      <li><strong>Evaluation:</strong> Prefer <strong>stratified k-fold CV</strong> (report mean ± sd) over a single split for stability.</li>
      <li><strong>Label hygiene:</strong> Keep genre strings consistent (e.g., <code>hiphop</code> vs <code>hip_hop</code>).</li>
    </ol>
    <p class="muted">I’m intentionally preserving the original code so the paper’s results remain reproducible; these notes document what I’d improve next.</p>
  </section>

  <footer style="margin:2rem 0 3rem; color:#6b7280;">
    <p>Prepared by Anshul — Original work graded at 94% in course; this README adds context and transparency for admissions.</p>
  </footer>
</main>
</body>
</html>
