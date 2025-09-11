import React from 'react'

import { Layout } from '../components/layout'
import { Hero } from '../components/hero'
import { HeroIllustration } from '../components/hero-illustration'

export default function HomePage() {
  return (
    <Layout>
      <Hero
        title="NuSkill"
        content="NuSkill is an Intuitive platform to not only learn new skills, but to also master accountability! Sign up with your Coinbase crypto-wallet id!"
        illustration={<HeroIllustration />}
      />
    </Layout>
  )
}
