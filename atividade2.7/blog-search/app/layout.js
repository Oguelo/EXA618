export const metadata = {
  title: 'Blog Search',
  description: 'Sistema de busca de mensagens',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body style={{ margin: 0, backgroundColor: 'black' }}>
        {children}
      </body>
    </html>
  )
}