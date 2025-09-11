import React from 'react'

import { Layout } from '../components/layout'
import { Article, ArticleContent, ArticleMedia } from '../components/article'

export default function ContactPage() {
  return (
    <Layout>
      <Article>
        <ArticleContent title="Contact">
          &nbsp; 
          <h4>Maanav Modi</h4>
          <p>maanavmodi@arizona.edu</p>
          <h4>Francisco Figueroa</h4>
          <p>ffigueroa@arizona.edu</p>
          <h4>Marissa Dicochea</h4>
          <p>mgd3@arizona.edu</p>
          <h4>Jake Thomason</h4>
          <p>jsthomason94@arizona.edu</p>
          <h4>Anshul Hallur</h4>
          <p>ahallur@arizona.edu</p>
        </ArticleContent>

        <ArticleMedia>
          <img src="https://picsum.photos/420/640" alt="Lorem Picsum" />
        </ArticleMedia>
      </Article>
    </Layout>
  )
}
