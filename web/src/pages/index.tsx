import Header from '../components/Header'
import { BodyContainer, ImgContainer, Main } from '../styles/pages/home'

import { api } from '../services/api'
import onibus from '../assets/img/onibus.webp'
import reitoria from '../assets/img/reitoria.png'
import { useEffect, useState } from 'react'
import { linha, response_linha } from '../types/api/linha'
import Table from '../components/Table'
import TableRow from '../components/TableRow'
import { Bus, CaretRight, Info } from 'phosphor-react'
import { Footer } from '../styles/global'
import { useRouter } from 'next/router'
import { GetServerSideProps, GetServerSidePropsContext } from 'next'

export default function Home({ linhas }) {
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
              <h1>Bem-vindo ao Moovooca</h1>
              <h3 className='lead'>Linhas de Ônibus dos Campus UFC</h3>
            </div>

            <Table header={['Linhas']}>
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
              <TableRow data={{
                info:
                  <a onClick={() => goTo('/linhas?page=1')}>
                    Ver mais
                    <CaretRight size={18} color="#276749" weight="bold" />
                  </a>
              }} />
            </Table>
          </section>

          <br />

          <section>
            <h3>Sobre o projeto</h3>
            <p>O projeto "moovooca" é uma iniciativa criada pelos estudantes do curso Pet Computação da Universidade Federal do Ceará (UFC), Pedro Yuri e Cauan Victor, com o objetivo de fornecer informações gerais sobre os ônibus que param na UFC e, assim, auxiliar os estudantes no seu deslocamento pela cidade.</p>

            <br />

            <h3>Como funciona?</h3>
            <p>O sistema é acessível através de um site na internet e conta com uma interface simples e fácil de usar. Nele, é possível selecionar a linha de ônibus desejada e visualizar as informações de horários de partida e chegada, além de ter acesso a um mapa com o trajeto completo da linha.

              O projeto "moovooca" já está em funcionamento e tem sido muito bem recebido pela comunidade estudantil da UFC. Com sua interface intuitiva e informações precisas, o sistema tem ajudado muitos estudantes a planejar melhor suas rotas de transporte, evitando atrasos e transtornos no seu dia a dia.

              Em resumo, o "moovooca" é um projeto que exemplifica a importância da tecnologia na solução de problemas cotidianos. A iniciativa dos estudantes da UFC Pedro Yuri e Cauan Victor tem o potencial de melhorar a vida dos estudantes que precisam se deslocar diariamente pela cidade e é uma inspiração para outros jovens que buscam fazer a diferença em sua comunidade através da tecnologia.</p>
          </section>
        </BodyContainer>
      </Main>
    </>
  )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { data: linha } = await api.get(`/linha_sentidos?page=1`);

  return {
    props: {
      linhas: linha.data
    }
  }
}