import React from 'react'
import classnames from 'clsx'

const SOCIAL_LINKS = [

]

export function SocialLinks({ className }) {
  return (
    <ul className={classnames('list-reset', className)}>
      {SOCIAL_LINKS.map((link) => (
        <SocialLinkItem key={link.name} link={link} />
      ))}
    </ul>
  )
}

export function SocialLinkItem({ link }) {
  const { name, url, svg } = link

  return (
    <li className="ml-4">
      <a href={url}>
        <span className="sr-only">{name}</span>
        <div dangerouslySetInnerHTML={{ __html: svg }} />
      </a>
    </li>
  )
}
