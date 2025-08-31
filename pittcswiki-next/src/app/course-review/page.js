
import React from 'react';
import Layout from '../../components/Layout';
import Head from 'next/head';

export default function CourseReviewPage() {
  return (
    <Layout>
      <Head>
        <title>Review a Pitt Course</title>
      </Head>
      <iframe
        title="Review a Course"
        src="https://docs.google.com/forms/d/e/1FAIpQLSfg2dNHW2sPBW2u40SqNFq_DAeRH1qg4NE5gIZQH0X4leqGvQ/viewform?embedded=true"
        width="100%"
        height="1674"
        frameBorder="0"
        marginHeight="0"
        marginWidth="0"
      >
        Loading…
      </iframe>
    </Layout>
  );
}
