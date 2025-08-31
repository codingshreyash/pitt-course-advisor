// this code is confusing because its like an interview question,
// given a flat list of urls, construct a tree diagram, and ensure no
// broken links contained in the urls

// this is used both to make the /sitemap page and also for unit tests

// this is the worst code in the whole repo, hard to read, bad names

const isAnchorLink = (link) => {
  // link to a section in the same markdown document
  // also known as anchor links or "links to heading id"
  return link.charAt(0) === '#'; // start with a #
}

const isExternalLink = (link) =>
  link.substring(0, 3) === "www" ||
  link.substring(0, 4) === "http" ||
  link.substring(0, 4) === "mail"

// clean link to a standard format. convert relative links to full links.
// check for errors (like an invalid url)
const convertLinkToFullPath = (link) => {
  link = cleanSiteLink(link)
  if (link[0] === ".") {
    return {
      error:
        "We do not support relative linking. Look at PR #162 for more details. ",
    }
  }
  // links can be malformed
  if (link[0] !== "/" && !isExternalLink(link)) {
    return { error: "This link is malformed" }
  }
  // links can have "/index" at the end
  return cleanSiteLink(link)
}

// Make sure the siteMap set and the links are formatted the same way
const cleanSiteLink = (link) => {
  let clean = link.toLowerCase()
  if (link.charAt(link.length - 1) !== "/") {
    clean += "/"
  }
  // some links link to headings, delete the heading
  // some links my have "index" at the end
  return clean.replace(/index$/g, "").replace(/#\w*\/$/g, "")
}

/*
Input 
sites: [ slug1, slug2, slug3, ...]
pages: [{ slug: ___, rawMarkdownBody: ___, title: ____ }]
*/
function siteGraphGenerator(sites, pages) {
  const errors = []
  const siteMap = sites.reduce((map, link) => {
    map[cleanSiteLink(link)] = true
    return map
  }, {})
  const siteNodes = pages.map((node) => {
    return {
      id: cleanSiteLink(node.slug),
      slug: node.slug,
      links: node.links, // node.links is defined during tests
      title: node.title,
      fields: {
        isIndexPage: node.fields && node.fields.isIndexPage,
      },
    }
  })

  const nodeMap = { ...siteMap }
  const tree = { children: {} }
  const nodes = []
  siteNodes.forEach((node) => {
    // turn the list of slugs ex: [/academics, /academics/minors, /academics/minors/stat, /skills]
    // into a tree
    const parts = node.id.substring(1).replace(/\/$/g, "").split("/")
    if (parts.length === 1) {
      tree.children[parts[0]] = {
        ...node,
        children: !!tree.children[parts[0]]
          ? tree.children[parts[0]].children
          : {},
      }
    } else {
      let currentBranch = tree
      for (let p = 0; p < parts.length - 1; p++) {
        const currentDir = parts[p]
        if (!currentBranch.children[currentDir]) {
          currentBranch.children[currentDir] = { children: {} }
        }
        currentBranch = currentBranch.children[currentDir]
      }
      let finalPart = parts[parts.length - 1]
      const childrenForCurrentBranch = currentBranch.children[finalPart]
        ? currentBranch.children[finalPart].children
        : {}
      currentBranch.children[finalPart] = {
        ...node,
        children: childrenForCurrentBranch,
      }
      nodeMap[node.id] = { ...node, children: childrenForCurrentBranch }
    }

    if (node.links) {
      // recursively check all links !
      node.links.forEach((link) => {
        if (isAnchorLink) return; // skip anchor links, use bash script validator instead
        const parsedLink = convertLinkToFullPath(link)
        if (parsedLink.error) {
          errors.push({
            file: node.slug,
            brokenLink: link,
            msg: parsedLink.error,
          })
        } else {
          if (!isExternalLink(parsedLink) && !siteMap[parsedLink]) {
            errors.push({
              file: node.slug,
              brokenLink: link,
              msg: "Was not in the list of pages",
            })
          }
        }
      })
    }
    nodes.push(node)
  })

  // this is turning {skills: {children: {}}, academics: {children: { studyabroad: {} }, }} into
  // [{id: skils, children: [...], {id: academics, children: [...]}
  const recursiveTreeSetToTreeArray = (tree) => {
    if ((tree && !tree.children) || !tree) return []
    return Object.keys(tree.children).map((key) => {
      const node = tree.children[key]
      // If no title is set, its either no title in the frontmatter, or this page is a javacsript
      // page in src/pages
      if (!node.title) {
        node.title = key.charAt(0).toUpperCase() + key.substring(1)
        if (!siteMap[node.slug]) {
          errors.push({
            file: node.slug,
            error:
              "If this is a folder, are you missing a 'index.md' file in this folder? Or if this is a file, are you missing the frontmatter and title?",
          })
        }
      }
      return {
        ...node,
        children: recursiveTreeSetToTreeArray(node),
      }
    })
  }

  const treeStructure = {
    children: recursiveTreeSetToTreeArray(tree),
  }

  return {
    nodes,
    tree: treeStructure,
    errors,
  }
}

module.exports = {
  siteGraphGenerator,
}
