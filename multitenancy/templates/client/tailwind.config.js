module.exports = {
    content: ['./src/**/*.{js,jsx,ts,tsx}'],
    darkMode: 'class',
    theme: {
      fontFamily: {
        display: ['Open Sans', 'sans-serif'],
        body: ['Open Sans', 'sans-serif'],
      },
      extend: {
        fontSize: {
          14: '14px',
        },
        zIndex: {
          '100': '100',
          '200': '200',
          '300': '300',
          '400': '400',
        },
        backgroundColor: {
          'main-bg': '#FAFBFB',
          'main-dark-bg': '#20232A',
          'secondary-dark-bg': '#33373E',
          'light-gray': '#F7F7F7',
          'quarter-transparent': 'rgba(0, 0, 0, 0.9)',
          'half-transparent': 'rgba(0, 0, 0, 0.5)',
          'semi-transparent': 'rgba(0, 0, 0, 0.2)',
          'semi-transparent': 'rgba(0, 0, 0, 0.2)',
        },
        borderWidth: {
          1: '1px',
        },
        borderColor: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        width: {
          400: '400px',
          450: '450px',
          500: '500px',
          600: '600px',
          760: '760px',
          780: '780px',
          800: '800px',
          1000: '1000px',
          1200: '1200px',
          1400: '1400px',
        },
        height: {
          73: '19rem',
          80: '80px',
          95: '22rem',
          98:'26rem',
          100:'30rem',
          164:'32rem',
          192:'34rem',
          200:'36rem',
          '6/10':"60%",
        },
        minHeight: {
          590: '590px',
        },
        backgroundSize: {
          'auto': 'auto',
          'cover': 'cover',
          'contain': 'contain',
          '50%': '50%',
          '16': '4rem',
        },
        borderRadius:{"100%":"100%"},
        backgroundImage: {
          'hero-pattern':
            "url('https://demos.wrappixel.com/premium-admin-templates/react/flexy-react/main/static/media/welcome-bg-2x-svg.25338f53.svg')",
        },
      },
    },
    plugins: [],
  };