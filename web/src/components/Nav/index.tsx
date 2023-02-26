import { useRouter } from "next/router";
import { NavButton, NavContainer } from "./styles";
import { Bell, House, PaperPlaneTilt } from 'phosphor-react';

import { NavProps } from "../../types/components/nav";

export default function Nav({ isNavOpen }: NavProps) {
  const router = useRouter();
  const page = router.pathname.split("/")[1];

  function goTo(route: string) {
    router.push(route);
  }

  return (
    <NavContainer isNavOpen={isNavOpen}>
      <div className="linkContainer">
        <ul>
          <NavButton active={page === '' && true} onClick={() => goTo('/')}>
            <House size={20} weight={page === '' ? 'fill' : 'regular'} color="#2f855a" />
            <span>Início</span>
          </NavButton>
        </ul>
      </div>
    </NavContainer>
  )
}