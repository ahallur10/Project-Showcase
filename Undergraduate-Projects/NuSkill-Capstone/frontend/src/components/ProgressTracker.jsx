import { useState } from "react";

export default function ProgressTracker({ uid }) {
  const [percent, setPercent] = useState(0);
  const [msg, setMsg] = useState("");

  async function save() {
    const r = await fetch("/api/tutorials/progress", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ uid, tutorial_id: 1, percent })
    });
    const j = await r.json();
    if (j.ok) setMsg(`Saved: ${percent}%`);
  }

  async function refund() {
    const r = await fetch("/api/tutorials/refund", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ uid })
    });
    const j = await r.json();
    if (j.ok) setMsg(`Refunded $${j.refunded}`);
    else setMsg(j.error || "No refundable deposit");
  }

  return (
    <div>
      <input type="number" min="0" max="100" value={percent} onChange={e=>setPercent(Number(e.target.value))} />
      <button onClick={save}>Save Progress</button>
      <button onClick={refund}>Refund</button>
      <p>{msg}</p>
    </div>
  );
}
