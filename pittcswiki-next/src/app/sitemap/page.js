import React from 'react';
import Layout from '../../components/Layout';
import Head from 'next/head';
import SitemapList from '../../components/sitemap-list';
import Link from 'next/link';
import { siteGraphGenerator } from '../../utils/sitegraph-generator';
import path from 'path';
import { promises as fs } from 'fs';
import matter from 'gray-matter';

export async function getStaticProps() {
  const guidesDirectory = path.join(process.cwd(), 'pittcswiki/src/guides');
  const files = await fs.readdir(guidesDirectory, { recursive: true });

  const markdownFiles = files.filter(file => file.endsWith('.md') || file.endsWith('.mdx'));

  const posts = await Promise.all(markdownFiles.map(async (file) => {
    const filePath = path.join(guidesDirectory, file);
    const fileContent = await fs.readFile(filePath, 'utf8');
    const { data } = matter(fileContent);

    const relativePath = path.relative(guidesDirectory, filePath);
    const slug = `/${relativePath.replace(/\\/g, '/').replace(/\.mdx?$/, '')}/`;

    return {
      frontmatter: data,
      fields: { slug },
    };
  }));

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
    { slug: '/sitemap/', title: 'Sitemap' },
  ]));

  return {
    props: {
      sitemapTree: tree,
    },
  };
}

const SitemapPage = ({ sitemapTree }) => {
  return (
    <Layout>
      <Head>
        <title>Sitemap</title>
      </Head>
      <h1>Site Map</h1>
      <p>
        This lists every page on the wiki! If you are feeling overwhelmed, check
        out the <Link href="/guides/">guides listing page</Link>, or try using the
        search in the top right corner.
      </p>
      <SitemapList tree={sitemapTree} />
      <div className="mb-10"></div>
    </Layout>
  );
};

export default SitemapPage;
