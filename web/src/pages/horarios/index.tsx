import { useRouter } from "next/router";
import Header from "../../components/Header";
import { api } from "../../services/api";
import { BodyContainer, Main, StopContainer } from "../../styles/pages/horarios";
import { ArrowUpRight, Bus, CaretDown, MapPin } from "phosphor-react";
import GoogleMapReact from 'google-map-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { sentido } from "../../types/api/sentido";
import { GetServerSidePropsContext } from "next";
import { HorarioProps } from "../../types/pages/Horario";
import Head from "next/head";
import Table from "../../components/Table";
import { viagem } from "../../types/api/viagem";
import TableRow from "../../components/TableRow";

export default function Horario({ linha, sentido, sentidos, viagens }: HorarioProps) {
  const router = useRouter()

  function goTo(path: string) {
    router.push(path)
  }

  const defaultProps = {
    center: {
      lat: -3.7765124,
      lng: -38.5637712
    },
    zoom: 17
  };


  return (
    <>
      <Head>
        <title>Rota da linha {linha.cod} {linha.nome} - Moovooca</title>
        <meta name='description' content='Linhas de Ônibus dos Campus UFC' />
      </Head>
      <Main>
        <Header />
        <BodyContainer>
          <div className="lineHeader">
            <h3 className="regular">Linha</h3>
            <div className="lineHeaderContainer">
              <h1>
                <span>
                  <Bus weight='regular' color="#276749" />
                  {linha.cod}
                </span>
                {linha?.nome}
              </h1>
              <DropdownMenu.Root>
                <DropdownMenu.Trigger asChild={true} className="DropdownMenuButton">
                  <button>Sentido {sentido.sentido} <CaretDown size={16} weight="bold" color="rgba(0, 0, 0, 0.8)" /></button>
                </DropdownMenu.Trigger>

                <DropdownMenu.Portal>
                  <DropdownMenu.Content className="DropdownMenuContent" sideOffset={5}>
                    <DropdownMenu.Arrow className="DropdownMenuArrow" />

                    {sentidos.map((sentido: sentido) => (
                      <DropdownMenu.Item className="DropdownMenuItem" key={sentido.id} onClick={() => goTo(`/horarios?lid=${linha.id}&sid=${sentido.id}`)}>
                        <DropdownMenu.Item className="DropdownMenuItemIndicator" asChild={false}>
                          <ArrowUpRight size={14} weight="bold" color="rgba(0, 0, 0, 0.8)" />
                        </DropdownMenu.Item>
                        Sentido {sentido.sentido}
                      </DropdownMenu.Item>
                    ))}

                  </DropdownMenu.Content>
                </DropdownMenu.Portal>
              </DropdownMenu.Root>
            </div>
            <hr />
          </div>


          <div className="mainContainer">
            <div className="lineContainer">
              <div className="infoContainer">
                <h3>Horários</h3>
                <div className="stopsNearContainer">
                  <div className="iconContainer">
                    <MapPin size={16} weight="fill" color="#2f855a" />
                  </div>

                  <div className="stopsNearText">
                    <span>Para próximo de: </span>
                    <span>{linha.campus}</span>
                  </div>
                </div>

                <div className="tripContainer">
                  <Table header={[]}>
                    {viagens.map((viagem: viagem) => {
                      return (
                        <TableRow key={viagem.id} data={{
                          linha:
                            <button onClick={() => goTo(`/linha?id=${linha.id}&sid=${linha.sentidos[0].id}`)}>
                              <div className='firstContainer'>
                                <span><Bus size={18} color="#2f855a" weight="bold" />{linha.cod}</span>
                                {viagem.origem}
                              </div>
                            </button>,
                        }} />
                      )
                    })}
                  </Table>
                </div>
              </div>
            </div>
            <br />
          </div>
        </BodyContainer>
      </Main>
    </>
  )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { lid, sid } = context.query;

  const { data: linha } = await api.get(`/linha?id=${lid}`);
  const { data: sentido } = await api.get(`/sentido?id=${sid}`);
  const { data: sentidos } = await api.get(`/sentidos?linha=${linha.id}`);
  const { data: viagens } = await api.get(`/viagens?linha=${lid}&sentido=${sid}`)

  return {
    props: {
      linha: linha,
      sentido: sentido,
      sentidos: sentidos,
      viagens: viagens
    }
  }
}