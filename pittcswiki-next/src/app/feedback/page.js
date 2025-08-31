
import React from 'react';
import Layout from '../../components/Layout';
import Head from 'next/head';

export default function FeedbackPage() {
  return (
    <Layout>
      <Head>
        <title>Feedback + Q&A</title>
      </Head>
      <div>
        <iframe
          title="Feedback and Q&A"
          src="https://docs.google.com/forms/d/e/1FAIpQLSfijKV1sHF7QGWYc6UzIbUuIIntDOPbyqdrzXg-snHeBN_qNg/viewform?embedded=true"
          width="100%"
          height="800"
          frameBorder="0"
          marginHeight="0"
          marginWidth="0"
        >
          Loading…
        </iframe>
      </div>
    </Layout>
  );
}
