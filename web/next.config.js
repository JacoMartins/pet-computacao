/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,

  // images: {
  //   remotePatterns: [
  //     {
  //       protocol: 'https',
  //       hostname: 'avatars.githubusercontent.com',
  //       port: '**',
  //       pathname: '**',
  //     },
  //     {
  //       protocol: 'https',
  //       hostname: 'media.lincdn.com',
  //       port: '**',
  //       pathname: '**',
  //     },
  //     {
  //       protocol: 'https',
  //       hostname: 'i.pinimg.com',
  //       port: '**',
  //       pathname: '**',
  //     },
  //     {
  //       protocol: 'https',
  //       hostname: 'i.imgur.com',
  //       port: '**',
  //       pathname: '**',
  //     }
  //   ],
  // }

  images: {
    domains: [
      'avatars.githubusercontent.com',
      'media.licdn.com',
      'i.pinimg.com',
      'i.imgur.com',
      'st2.depositphotos.com'
    ],
  }
}

module.exports = nextConfig;