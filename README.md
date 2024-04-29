<h1>PassMan - Password Manager</h1>

<p>PassMan is a simple password manager application written in Python. It allows users to securely store and retrieve passwords for different services.</p>

<h2>Features</h2>

<ul>
  <li><strong>User Authentication:</strong> Users can sign up and log in securely.</li>
  <li><strong>Password Storage:</strong> Passwords are encrypted and stored in an SQLite database.</li>
  <li><strong>Service-based Retrieval:</strong> Retrieve passwords for specific services.</li>
</ul>

<h2>Installation</h2>

<ol>
  <li><strong>Clone the repository:</strong></li>
  <pre><code>git clone https://github.com/offseckalki/PassMan.git</code></pre>

  <li><strong>Navigate to the project directory:</strong></li>
  <pre><code>cd PassMan</code></pre>

  <li><strong>Install dependencies:</strong></li>
  <pre><code>pip install -r requirements.txt</code></pre>

  <li><strong>Create a new SQLite database:</strong></li>
  <pre><code>touch passwords.db</code></pre>
</ol>

<h2>Usage</h2>

<ol>
  <li><strong>Run the application:</strong></li>
  <pre><code>python password_manager.py</code></pre>

  <li><strong>Use the GUI interface to sign up, log in, and manage passwords.</strong></li>
</ol>

<h2>Configuration</h2>

<ul>
  <li>Modify settings in <code>config.py</code> as needed.</li>
</ul>

<h2>Screenshots (Optional)</h2>

<p><img src="/screenshots/login.png" alt="Login Screen" /></p>
<p>Login Screen</p>

<p><img src="/screenshots/password_manager.png" alt="Password Manager Interface" /></p>
<p>Password Manager Interface</p>

<h2>Contributing</h2>

<p>Contributions are welcome! Please fork the repository and submit pull requests.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

<h2>Acknowledgements</h2>

<ul>
  <li><a href="https://cryptography.io/en/latest/">Cryptography</a> library</li>
  <li><a href="https://www.sqlite.org/">SQLite</a> database</li>
  <li>AI assistance in developing the GUI version</li>
</ul>
