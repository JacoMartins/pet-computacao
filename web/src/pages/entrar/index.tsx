import { useRouter } from "next/router";
import { Bus, CircleNotch } from "phosphor-react";
import { useState } from "react";
import { api } from "../../services/api";
import { Logo } from "../../styles/pages/criar";
import { Main } from "../../styles/pages/criar";

export default function CreateAccount() {
  const router = useRouter();

  const [identificador, setIdentificador] = useState<string>('');
  const [senha, setSenha] = useState<string>('');

  const [busy, setBusy] = useState<boolean>(false);

  const [error, setError] = useState<string>();

  function goTo(path:string){
    router.push(path)
  }

  return (
    <Main>
      <div className='formContainer'>
        <Logo>
          <Bus size={24} weight="regular" color="#276749" />
          <span>
            moovooca
          </span>
        </Logo>
        <h4>Entrar</h4>
        <form onSubmit={() => console.log('bababoi')}>
          <input type="text" placeholder="Nome de usuário ou email" onChange={event => setIdentificador(event.target.value)} />
          <input type="password" placeholder="Senha" onChange={event => setSenha(event.target.value)} />

          <div className="buttonContainer">
            <button type="button" onClick={() => goTo('/criar')}>
              Criar Conta
            </button>
            <button type="submit" className="createAccount">
              {busy ? <CircleNotch className="load" size={24} weight="regular" color="#fff" /> : 'Entrar'}
            </button>
          </div>
        </form>
        {error && <p>{error}</p>}
      </div>
    </Main>
  )
}