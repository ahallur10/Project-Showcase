import { useState } from "react";

export default function DepositWidget({ token }) {
  const [url, setUrl] = useState(null);
  async function startDeposit() {
    const r = await fetch("/api/payments/intent", {
      method:"POST",
      headers:{ "Content-Type":"application/json", Authorization:`Bearer ${token}` },
      body: JSON.stringify({ amount_usd: 10 })
    });
    const j = await r.json(); 
    if (j.ok) setUrl(j.pay_url);
  }
  return (
    <div>
      <button onClick={startDeposit}>Place $10 deposit</button>
      {url && <a href={url} target="_blank" rel="noreferrer">Complete Payment</a>}
    </div>
  );
}
