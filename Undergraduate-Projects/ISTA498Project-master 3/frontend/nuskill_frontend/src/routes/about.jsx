import React from 'react'

import { Layout } from '../components/layout'
import { Article, ArticleContent, ArticleMedia } from '../components/article'

export default function AboutPage() {
  return (
    <Layout>
      <Article>
        <ArticleContent title="About">
          <p>
          We believe education should be avaiable to all for free, and those who search for it should find it. Our mission is to
          streamline the process and costs of learning something new. 
          </p>
          <p>
          Sometimes we try something we don't like. Some enjoy programming and some don't... however, someone who doesn't enjoy coding should not lose money in search of a
              new passion. This would only discourage one to search for something new. Here, it is free if you make it to be, and when you reap the rewards you walk with a new fire or simply satisfy a curiosity.
          </p>
        </ArticleContent>

        <ArticleMedia>
          <img
            src="https://picsum.photos/420/640?grayscale"
            alt="Lorem Picsum"
          />
        </ArticleMedia>
      </Article>
    </Layout>
  )
}
