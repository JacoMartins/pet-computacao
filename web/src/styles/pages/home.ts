import { styled } from '../';

export const Main = styled('main', {
  height: '100%',
  maxWidth: '100%',
  display: 'flex',
  gap: '1rem',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  background: 'transparent',
  padding: '6.5rem 2.5rem'
});

export const BodyContainer = styled('div', {
  width: '100%',
  maxWidth: '68rem',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'left',
  alignItems: 'left',
  textAlign: 'left',

  '.welcomeSection': {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    gap: '0.5rem',
    
    '@media screen and (min-width: 720px)': {
      alignItems: 'left',
    },

    '@media screen and (max-width: 720px)': {
      flexDirection: 'column',
      justifyContent: 'left',
      alignItems: 'left',
    },

    '.imgContainer': {
      height: '20rem',
      width: '25rem',

      '@media screen and (max-width: 720px)': {
        height: '15rem',
        width: 'auto',
      },
    }
  }
});

export const ImgContainer = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  overflow: 'hidden',
  borderRadius: '0.5rem',
  marginBottom: '1rem',
  background: 'url("") no-repeat',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
});