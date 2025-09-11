import React from 'react'

import { Layout } from '../components/layout'
import { Article, ArticleContent, ArticleMedia } from '../components/article'

export default function FaqsPage() {
  return (
    <Layout>
      <Article>
        <ArticleContent title="FAQ's">
          <p><b>Q: How do I sign-up?</b></p>
          <p>A: We require you to have a Coinbase account as we process payments through their platform.</p>
          <p><b>Q: How do I access videos everyday?</b></p>
          <p>A: Once you login, it will prompt you to deposit for the day and once you deposit through Coinbase, you will be able to access the videos.</p>
          <p><b>Q: When will I receive what I earned back?</b></p>
          <p>A: Every night at 11:00PM MST, we go through each user's progress and deposit however much was earned back into
            their Coinbase account wallet.
          </p>


        </ArticleContent>

        <ArticleMedia>
          <img src="https://picsum.photos/420/640" alt="Lorem Picsum" />
        </ArticleMedia>
      </Article>
    </Layout>
  )
}
