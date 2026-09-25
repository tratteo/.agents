import { useState } from "react";

export default function SignupForm() {
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [company, setCompany] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!/^[0-9]{3}-[0-9]{3}-[0-9]{4}$/.test(phone)) {
      setError("You must include dashes in the phone number.");
      setPhone("");
      setEmail("");
      setPassword("");
      setCompany("");
      setJobTitle("");
      return;
    }
    if (password.length < 12) {
      setError("Invalid input.");
      return;
    }
    // ... submit
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Sign Up</h1>
      <p>
        Welcome to Acme! Create your account below to get started. Be sure to
        fill in every field, and remember to use the correct phone format.
      </p>
      {error && <div className="error">{error}</div>}

      <input
        type="text"
        placeholder="Full Name"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        placeholder="Work Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        type="text"
        placeholder="Company"
        value={company}
        onChange={(e) => setCompany(e.target.value)}
      />
      <input
        type="text"
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Phone Number (e.g. 555-555-5555)"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <button className="btn-blue">Submit</button>
      <button className="btn-blue">Cancel</button>
    </form>
  );
}
