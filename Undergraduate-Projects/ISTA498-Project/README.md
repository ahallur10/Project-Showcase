<h2>Introduction</h2>
<p>
NuSkill is a full-stack web application that introduces an <b>accountability model for online learning</b>. 
Users place cryptocurrency deposits before starting tutorials, which can be reclaimed upon completion, 
creating a financial incentive to follow through. The platform combines an intuitive learning interface 
with secure payment handling and balance tracking.
</p>

<hr>

<h2>Problem Statement</h2>
<p>
A common challenge in self-paced online learning is <b>lack of accountability</b>. Learners often sign up for 
tutorials but drop out before completing them. The question we explored was:
</p>
<blockquote>
How can we motivate users to complete online learning modules by aligning financial incentives with educational goals?
</blockquote>

<hr>

<h2>Solution</h2>
<ul>
<li>Using <b>cryptocurrency deposits</b> to create a tangible commitment.</li>
<li>Refunding deposits when tutorials are completed, rewarding persistence.</li>
<li>Providing a <b>secure backend</b> for handling deposits, withdrawals, and balances.</li>
<li>Offering a user-friendly <b>React.js frontend</b> for login, dashboard, and progress visualization.</li>
</ul>

<hr>

<h2>Methodology</h2>
<p>
NuSkill was developed as a collaborative capstone project. My role focused on:
</p>
<ul>
<li><b>Idea conception</b>: I initiated the accountability-through-crypto model, which became the foundation of the project.</li>
<li><b>Backend payment services</b>: Implemented Flask routes for deposits and balance tracking.</li>
<li><b>Coinbase integration</b>: Built the API flow to generate hosted checkout URLs, enabling deposits and refunds.</li>
<li><b>Database integration</b>: Connected payment services to Snowflake SQL for tracking balances.</li>
<li><b>Collaboration</b>: Partnered with teammates who extended the frontend (React.js, Vite/Tailwind) and cloud deployment (Google Cloud Run).</li>
</ul>

<hr>

<h2>How to Access and Run Locally</h2>
<p>To launch the application you must startup the frontend and backend independently</p>

<h3>Quick Setup</h3>
<ol>
<li>Clone this repository and navigate to the NuSkill project folder:
<pre><code>git clone https://github.com/&lt;your-username&gt;/Project-Showcase.git
cd Project-Showcase/Undergraduate-Projects/NuSkill-Capstone
</code></pre></li>

<li>Ensure you have <b>Python 3.10+</b>, <b>Node.js (LTS)</b>, and <b>npm</b> installed.</li>

<li>Set environment variable for mock mode (recommended for demo):
<pre><code>export USE_MOCK=1        # Windows PowerShell: $env:USE_MOCK="1"
</code></pre></li>

<li>Start the backend (Flask), then in a new terminal start the frontend (Vite/React).</li>
</ol>

<h3>Backend (Flask)</h3>
<pre><code>
cd project/backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
export USE_MOCK=1           # Windows: $env:USE_MOCK="1"
python main.py              # runs at http://127.0.0.1:8080
</code></pre>

<h3>Frontend (Vite + React.js)</h3>
<pre><code>
cd frontend/nuskill_frontend
npm install
npm run dev                 # runs at http://localhost:5173/nu-skill/
</code></pre>

<p><b>Note</b>: USE_MOCK=1 runs the app with mock data since the original Snowflake DB and Coinbase live keys are no longer active.</p>

<h3>Sign-In</h3>
<p>
Use the following demo credentials to log in when running in mock mode:
</p>

<ul>
  <li><b>Username:</b> <code>user_test_5</code></li>
  <li><b>Password:</b> <code>anything</code></li>
</ul>
<hr>

<h2>Tech Stack</h2>
<ul>
<li><b>Frontend</b>: React.js, Vite, Tailwind CSS</li>
<li><b>Backend</b>: Flask (Python), REST APIs</li>
<li><b>Database</b>: Snowflake SQL</li>
<li><b>Payments</b>: Coinbase Commerce + Wallet APIs (mock mode for demo)</li>
<li><b>Deployment</b>: Google Cloud Run</li>
</ul>

<hr>

<h2>Contributions (Anshul Hallur)</h2>
<ul>
<li>Conceived the accountability-through-crypto idea.</li>
<li>Implemented Coinbase Commerce integration for deposits and refunds.</li>
<li>Developed backend Flask routes for deposits, balances, and payment handling.</li>
<li>Integrated Snowflake SQL for balance tracking.</li>
<li>Supported team members with documentation and mock data setup.</li>
</ul>

<hr>

<h2>Screenshots</h2>
<p> <img width="1575" height="1064" alt="Screenshot 2025-09-10 at 9 52 24 PM" src="https://github.com/user-attachments/assets/2664562d-24db-4fa2-a61f-2fbd17b3033e" />
 </p>

 <p><img width="1443" height="1013" alt="Screenshot 2025-09-10 at 10 01 00 PM" src="https://github.com/user-attachments/assets/8d5717f1-71f6-4974-aefb-6966cfb6020b" />
</p>
