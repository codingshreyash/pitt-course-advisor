

import React from 'react';
import Layout from '../../components/Layout';
import Head from 'next/head';
import Link from 'next/link';
import SitemapList from '../../components/sitemap-list';
import { siteGraphGenerator } from '../../utils/sitegraph-generator';
import path from 'path';
import { promises as fs } from 'fs';
import matter from 'gray-matter';

const GuidesListing = ({ posts }) => {
  const guides = posts
    .filter((p) => p.excerpt)
    .map((post, index) => (
      <Link
        className="inline-block p-1 w-full text-gray-800 px-4 py-4 md:w-1/2"
        href={post.fields.slug}
        key={`g_${index}`}
      >
        <div className="border bg-gray-200 shadow-sm h-64 p-4 transition hover:bg-gray-600 hover:text-white hover:shadow-md">
          <h1>{post.frontmatter.title}</h1>
          <div>{post.frontmatter.guides_blurb}</div>
        </div>
      </Link>
    ));

  return <div className="flex flex-wrap -mx-4 -mt-4">{guides}</div>;
};

export async function getStaticProps() {
  const guidesDirectory = path.join(process.cwd(), 'pittcswiki/src/guides');
  const files = await fs.readdir(guidesDirectory, { recursive: true });

  const markdownFiles = files.filter(file => file.endsWith('.md') || file.endsWith('.mdx'));

  const posts = await Promise.all(markdownFiles.map(async (file) => {
    const filePath = path.join(guidesDirectory, file);
    const fileContent = await fs.readFile(filePath, 'utf8');
    const { data, excerpt } = matter(fileContent, { excerpt: true });

    // Construct slug based on file path relative to guidesDirectory
    const relativePath = path.relative(guidesDirectory, filePath);
    const slug = `/${relativePath.replace(/\\/g, '/').replace(/\.mdx?$/, '')}/`;

    return {
      frontmatter: data,
      fields: { slug },
      excerpt,
    };
  }));

  // Filter out posts that are not index pages or don't have guides_blurb
  const filteredPosts = posts.filter(post => {
    const isIndexPage = post.fields.slug.endsWith('/') && post.fields.slug.split('/').filter(Boolean).length > 0;
    return isIndexPage && post.frontmatter.guides_blurb;
  });

  // Sort posts by title
  filteredPosts.sort((a, b) => a.frontmatter.title.localeCompare(b.frontmatter.title));

  // Generate site graph for SitemapList
  const allSlugs = posts.map(post => post.fields.slug);
  const allPages = posts.map(post => ({
    slug: post.fields.slug,
    title: post.frontmatter.title,
  }));

  const { tree } = siteGraphGenerator(allSlugs, allPages.concat([
    { slug: '/about/', title: 'About' },
    { slug: '/guides/', title: 'Guides' },
    { slug: '/courses/', title: 'Course Exploration and Testimonials' },
    { slug: '/feedback/', title: 'Feedback' },
  ]));

  return {
    props: {
      guides: { nodes: filteredPosts },
      sitemapTree: tree,
    },
  };
}

export default function GuidesPage({ guides, sitemapTree }) {
  return (
    <Layout>
      <Head>
        <title>Guides</title>
      </Head>
      <h1>Guides</h1>
      <ul>
        <li>
          Considering the CS Major or a freshmen?{" "}
          <Link href="/academics/prospective">Click here</Link>
        </li>
        <li>
          Looking for course reviews? <Link href="/courses/">Click here</Link>
        </li>
        <li>
          Want to learn how to land internship and job offers?{" "}
          <Link href="/zero-to-offer/">Click here</Link>
        </li>
      </ul>
      <p>
        Below are collections of guides organized by topic. You can also use the
        search bar at the top right to search for articles, classes and more!
      </p>
      <GuidesListing posts={guides.nodes} />
      <p>
        If you ever have any questions or feedback, you can ask by visiting{" "}
        <Link href="/feedback">this link!</Link>
      </p>
      <div>
        <h2>Popular</h2>
        <ul>
          <li>
            <Link href={"/academics/scheduling"}>Scheduling</Link>
          </li>
          <li>
            <Link href={"/courses"}>Course Explorer</Link>
          </li>
          <li>
            <Link href={"/zero-to-offer"}>Zero to Offer</Link>
          </li>
        </ul>
      </div>
      <div className="mb-8">
        <h2>Full Guide Listing</h2>
        <SitemapList tree={sitemapTree} />
      </div>
      <p>
        Still curious about something but cannot find it? Please let us know and
        we can add it! <Link href="/feedback">Fill out this form.</Link>
      </p>
    </Layout>
  );
}

