import Header from '../../components/Header'
import { BodyContainer, Main } from '../../styles/pages/home'

import { api } from '../../services/api'
import { linha } from '../../types/api/linha'
import Table from '../../components/Table'
import TableRow from '../../components/TableRow'
import { Bus, CaretLeft, CaretRight } from 'phosphor-react'
import { Footer } from '../../styles/global'
import { useRouter } from 'next/router'
import { GetServerSidePropsContext } from 'next'
import { int } from '../../utils/convert'

export default function Linhas({ linhas, page, page_count }) {
  const router = useRouter()

  function goTo(path: string) {
    router.push(path)
  }

  return (
    <>
      <Main>
        <Header />
        <BodyContainer>
          <section className="welcomeSection">
            <div className="textContainer">
              <h1>Linhas</h1>
            </div>

            <Table header={[]}>
              <TableRow data={{
                info:
                  <div className='pagination'>
                    <span>Página {page} de {page_count}</span>
                    <div className='buttonContainer'>
                      {page > page_count &&
                        <button onClick={() => goTo(`/linhas?page=${int(page) - 1}`)}>
                          <CaretLeft size={18} color="#276749" weight="bold" />
                        </button>}
                      {page < page_count &&
                        <button onClick={() => goTo(`/linhas?page=${int(page) + 1}`)}>
                          <CaretRight size={18} color="#276749" weight="bold" />
                        </button>}
                    </div>
                  </div>
              }} />
              {linhas.map((linha: linha) => {
                return (
                  <TableRow key={linha.id} data={{
                    linha:
                      <button onClick={() => goTo(`/linha?id=${linha.id}&sentido=${linha.sentidos[0].id}`)}>
                        <div className='firstContainer'>
                          <span><Bus size={18} color="#2f855a" weight="bold" />{linha.cod}</span>
                          {linha.nome}
                        </div>
                        <div className='lastContainer'>
                          <span>Passa próximo de</span>
                          <a> </a>
                        </div>
                      </button>,
                  }} />
                )
              })}
            </Table>
          </section>
        </BodyContainer>
      </Main>
    </>
  )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { page } = context.query;

  const { data: linha } = await api.get(`/linha_sentidos?page=${page}`);
  const { data: contagem_linhas } = await api.get(`/linha_count`);

  const page_count = Math.ceil(int(contagem_linhas) / 10);

  return {
    props: {
      linhas: linha.data,
      page,
      page_count
    }
  }
}