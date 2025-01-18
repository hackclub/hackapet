import React, { useState } from 'react';

const EmailSignup = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure email is not empty and is valid
    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      setStatus({ type: 'error', message: 'Please enter a valid email address.' });
      return;
    }

    setIsSubmitting(true);
    setStatus(null); // Clear previous status message

    try {
      // Make a POST request to the serverless function to add the email
      const response = await fetch('/api/add-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus({ type: 'success', message: data.message });
      } else {
        setStatus({ type: 'error', message: data.message });
      }
    } catch (error) {
      setStatus({ type: 'error', message: 'Something went wrong. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mx-auto p-6 rounded-lg">      
      {status && (
        <div className={`text-center p-2 mb-4 ${status.type === 'error' ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
          {status.message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          className="p-2 mb-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-950"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={isSubmitting}
        />
        <button
          type="submit"
          className={`p-2 text-white rounded-md bg-lightPink ${isSubmitting ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Join the Slack'}
        </button>
      </form>
      <p className="text-darkPink">Not currently in the Hack Club Slack? Enter your email to get join instructions!</p>
    </div>
  );
};

export default EmailSignup;
