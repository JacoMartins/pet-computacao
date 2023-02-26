import { Bus, Gear, List, SignOut, User } from "phosphor-react";
import { RefObject, useEffect, useRef, useState } from "react";
import { HandleNav, HeaderContainer, LabelText, Logo } from "./styles";

import Nav from "../Nav";

import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import ProfileButton from "../ProfileButton";
import { NavButton } from "../Nav/styles";
import { HeaderProps } from "../../types/components/header";
import { useRouter } from "next/router";

export default function Header({}: HeaderProps) {
  const [scrollY, setScrollY] = useState(0);
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [headerHeight, setHeaderHeight] = useState(0);
  const router = useRouter();

  const [isLogged, setIsLogged] = useState(false);
  const profileImage = 'https://st2.depositphotos.com/5682790/10456/v/600/depositphotos_104564156-stock-illustration-male-user-icon.jpg';

  const isTransparent = scrollY === 0;

  const refs = {
    header: useRef() as RefObject<HTMLDivElement>,
  };

  function handleNav() {
    setIsNavOpen(!isNavOpen);
  }

  function goTo(route: string) {
    router.push(route);
  }

  useEffect(() => {
    setHeaderHeight(refs.header.current?.clientHeight || 0);

    window.addEventListener('scroll', () => {
      setScrollY(window.scrollY);
    });
  }, [refs.header]);

  return (
    <HeaderContainer ref={refs.header} isTransparent={isTransparent}>
      <div className='MainContainer'>

        <div className='LogoContainer'>
          <HandleNav onClick={handleNav} active={isNavOpen}>
            <List size={24} weight="fill" color="rgba(0, 0, 0, 0.85)" />
          </HandleNav>
          <Logo onClick={() => goTo('/')}>
            <Bus size={24} weight="regular" color="#276749"/>
            <span>
            moovooca
            </span>
          </Logo>
        </div>


        <div className="rightContainer">
          <Nav isNavOpen={isNavOpen} />
          {isLogged ? (
            <DropdownMenu.Root>
              <DropdownMenu.Trigger asChild={false} className="DropdownMenuButton">
                <ProfileButton main_name={'noname'} picture_profile={profileImage} />
              </DropdownMenu.Trigger>

              <DropdownMenu.Portal>
                <DropdownMenu.Content className="DropdownMenuContent" sideOffset={5}>
                  <DropdownMenu.Label className="DropdownMenuLabel" style={{ paddingLeft: '0.5rem' }}>
                    <LabelText>
                      Jacó Martins
                    </LabelText>
                  </DropdownMenu.Label>
                  <DropdownMenu.Arrow className="DropdownMenuArrow" />
                  <DropdownMenu.Item className="DropdownMenuItem">
                    <DropdownMenu.Item className="DropdownMenuItemIndicator" asChild={false}>
                      <User size={14} weight="bold" color="rgba(0, 0, 0, 0.8)" />
                    </DropdownMenu.Item>
                    Meu perfil
                  </DropdownMenu.Item>

                  <DropdownMenu.Separator className="DropdownMenuSeparator" />

                  <DropdownMenu.Item className="DropdownMenuItem">
                    <DropdownMenu.Item className="DropdownMenuItemIndicator" asChild={false}>
                      <Gear size={14} weight="bold" color="rgba(0, 0, 0, 0.8)" />
                    </DropdownMenu.Item>
                    Configurações
                  </DropdownMenu.Item>

                  <DropdownMenu.Item className="DropdownMenuItem">
                    <DropdownMenu.Item className="DropdownMenuItemIndicator" asChild={false}>
                      <SignOut size={14} weight="bold" color="rgba(0, 0, 0, 0.8)" />
                    </DropdownMenu.Item>
                    Sair
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
          ) : (
            <>
              <NavButton onClick={() => setIsLogged(true)} isSignUp={false}>Criar conta</NavButton>
              <NavButton onClick={() => setIsLogged(true)} isSignUp={true}>Entrar</NavButton>
            </>
          )}
        </div>
      </div>
    </HeaderContainer>
  )
}