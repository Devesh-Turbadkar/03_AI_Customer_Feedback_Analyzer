const $ = (id) => document.getElementById(id);
async function request(url, options={}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}
async function loadStats() {
  const data = await request("/api/analytics");
  $("total").textContent = data.total_reviews;
  $("positive").textContent = data.sentiment_counts.Positive;
  $("negative").textContent = data.sentiment_counts.Negative;
  $("neutral").textContent = data.sentiment_counts.Neutral;
}
function esc(value="") {
  return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
async function loadReviews() {
  const params = new URLSearchParams();
  if ($("search").value.trim()) params.set("search", $("search").value.trim());
  if ($("sentiment").value) params.set("sentiment", $("sentiment").value);
  const rows = await request("/api/reviews?" + params.toString());
  $("reviews").innerHTML = rows.length ? rows.map(r => `
    <article class="review">
      <div class="review-top"><strong>${esc(r.customer_name || "Customer")} · ${esc(r.source || "Unknown source")}</strong><span class="pill ${r.sentiment}">${r.sentiment}</span></div>
      <p class="review-text">${esc(r.review_text)}</p>
      <div class="details"><b>Summary:</b> ${esc(r.short_summary)}<br>
      <b>Positive:</b> ${esc(r.positive_points.join(", ") || "—")}<br>
      <b>Concerns:</b> ${esc(r.negative_points.join(", ") || "—")}<br>
      <b>Topics:</b> ${esc(r.topics.join(", ") || "—")}<br>
      <b>Suggestions:</b> ${esc(r.improvement_suggestions.join("; ") || "—")}</div>
    </article>`).join("") : '<p class="muted">No reviews found.</p>';
}
async function refresh() { await Promise.all([loadStats(), loadReviews()]); }
$("review-form").addEventListener("submit", async e => {
  e.preventDefault(); const button=e.submitter; button.disabled=true; $("message").textContent="Analyzing with Gemini...";
  try {
    await request("/api/reviews",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({customer_name:$("customer").value || null,source:"Manual",review_text:$("review").value})});
    $("review").value=""; $("customer").value=""; $("message").textContent="Review analyzed and saved.";
    await refresh();
  } catch(err) {$("message").textContent=err.message;} finally {button.disabled=false;}
});
$("csv-form").addEventListener("submit", async e => {
  e.preventDefault(); const button=e.submitter; button.disabled=true; $("message").textContent="Processing CSV. Each row is sent for AI analysis...";
  try {
    const form=new FormData(); form.append("file",$("csv").files[0]);
    const data=await request("/api/reviews/bulk",{method:"POST",body:form});
    $("message").textContent=`Saved ${data.saved_count} reviews; ${data.error_count} row errors.`;
    $("csv").value=""; await refresh();
  } catch(err) {$("message").textContent=err.message;} finally {button.disabled=false;}
});
$("insight-btn").addEventListener("click", async e => {
  const button=e.currentTarget; button.disabled=true; $("insights").textContent="Generating insights...";
  try {
    const d=await request("/api/insights",{method:"POST"});
    const section=(title,items)=>`<h3>${title}</h3><ul>${items.map(x=>`<li>${esc(x)}</li>`).join("") || "<li>None identified</li>"}</ul>`;
    $("insights").innerHTML=`<p>${esc(d.summary)}</p>${section("Common complaints",d.common_complaints)}${section("Customer strengths",d.strengths)}${section("Recommendations",d.recommendations)}<small>Based on ${d.reviews_analyzed} reviews.</small>`;
  } catch(err) {$("insights").textContent=err.message;} finally {button.disabled=false;}
});
let searchTimer; $("search").addEventListener("input",()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>loadReviews().catch(e=>$("reviews").textContent=e.message),300);});
$("sentiment").addEventListener("change",()=>loadReviews().catch(e=>$("reviews").textContent=e.message));
refresh().catch(e=>$("reviews").textContent=e.message);
