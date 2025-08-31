import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

import Layout from '../components/Layout';
import Head from 'next/head';

const IndexPage = () => (
  <Layout>
    <Head>
      <title>Home</title>
    </Head>
    <div>
      <div className="landing-image">
        <img alt="" src="/pittcampus.jpg" className="w-auto md:w-full" />
      </div>
      <div className="max-w-4xl mx-auto">
        <div className="md:mt-24 flex">
          <div className="hidden md:block self-end h-64 bg-white p-6 shadow-2xl w-1/2 border">
            <h1>The Pitt CS Wiki</h1>
            <p>
              A collection of course testimonials, guides, career prep
              resources, and much more!
            </p>
            <Link
              href="/guides/"
              className="btn inline-flex bg-pittgold items-center"
            >
              Get Started {rightArrowSvg}
            </Link>
          </div>
          <div className="w-1/2">
            <img
              src="/logo.svg"
              className="ml-auto max-w-sm -mb-12"
              alt="Pitt CS Wiki Logo"
            />
          </div>
        </div>
        <div className="md:hidden mt-12">
          <h1>The Pitt CS Wiki</h1>
          <p>
            A collection of course testimonials, guides, career prep resources,
            and much more!
          </p>
          <Link
            href="/guides/"
            className="btn inline-flex bg-pittgold items-center"
          >
            Get Started {rightArrowSvg}
          </Link>
        </div>
        <LinkPanel />
      </div>
    </div>
  </Layout>
);

const LinkPanel = () => {
  const router = useRouter();
  return (
    <div
      id="blurb-grid"
      className="my-12 flex flex-col items-center flex-wrap md:flex-row justify-center"
    >
      <div
        className="quick-blurb"
        onClick={() => router.push("/courses/")}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            router.push("/courses/");
          }
        }}
        role="button"
        tabIndex={0}
      >
        <img
          className="w-16 mx-auto"
          alt="Courses from the Noun Project"
          src="/icons/courses.svg"
        />
        <h3>Course Explorer</h3>
        <p>
          Find the right course for you! Professor reviews, course testimonials,
          and more. <Link href="/courses/">Learn more.</Link>
        </p>
      </div>
      <div
        className="quick-blurb"
        onClick={() => router.push("/guides/")}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            router.push("/guides/");
          }
        }}
        role="button"
        tabIndex={0}
      >
        <img src="/icons/guides.svg" alt="guide by Youmena from the Noun Project" />
        <h3>Guides</h3>
        <p>
          View all of our articles organized by topic. Check out popular ones
          and recently updated. <Link href="/guides/">Learn more.</Link>
        </p>
      </div>
      <div
        className="quick-blurb"
        onClick={() => router.push("/career/")}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            router.push("/career/");
          }
        }}
        role="button"
        tabIndex={0}
      >
        <img
          src="/icons/career.svg"
          alt="career by Thuy Nguyen from the Noun Project"
        />
        <h3>Career</h3>
        <p>
          Read our carefully curated tips on how to land job offers and succeed
          in your career. <Link href="/career/">Learn more.</Link>
        </p>
      </div>
      <div
        className="quick-blurb"
        onClick={() => router.push("/academics/")}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            router.push("/academics/");
          }
        }}
        role="button"
        tabIndex={0}
      >
        <img
          src="/icons/academic.svg"
          alt="academic by pam pyke from the Noun Project"
        />
        <h3>Academics</h3>
        <p>
          Thinking about a double major? Not sure what classes to take when?
          Curious about research? Learn the answers to all of your questions
          here! <Link href="/academics/">Learn more.</Link>
        </p>
      </div>
      <div
        className="quick-blurb"
        onClick={() => router.push("/sitemap/")}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            router.push("/sitemap/");
          }
        }}
        role="button"
        tabIndex={0}
      >
        <img
          src="/icons/sitemap.svg"
          alt="Sitemap by Adrien Coquet from the Noun Project"
        />
        <h3>Sitemap</h3>
        <p>
          We have a lot of content and its growing. Click here to see a list of
          everything we have. <Link href="/sitemap/">Learn more.</Link>
        </p>
      </div>
    </div>
  );
};

const rightArrowSvg = (
  <svg
    stroke="currentColor"
    className="ml-1"
    fill="currentColor"
    strokeWidth="0"
    viewBox="0 0 24 24"
    height="1em"
    width="1em"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"></path>
  </svg>
);

export default IndexPage;