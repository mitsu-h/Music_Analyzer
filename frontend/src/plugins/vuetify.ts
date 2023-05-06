// vuetify.ts
import { createVuetify } from 'vuetify';
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import * as labs from 'vuetify/labs/components';
import { aliases, mdi } from 'vuetify/lib/iconsets/mdi-svg';
import {mdiMagnify} from '@mdi/js';
// import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

const musicAnalyzerTheme = {
  dark: false,
  colors:{
      background: "#333333",
      surface: "#4e4e4e",
      primary: "#d9d9d9",
      secondary: "#d9d9d9",
      error: '#B00020',
      info: '#2196F3',
     success: '#4CAF50',
      warning: '#FB8C00',
    },
}

const vuetify = createVuetify({
  components:{
    ...components,
    ...labs
  },
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases:{
      ...aliases,
      magnify:mdiMagnify
    },
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'musicAnalyzerTheme',
    themes: {
      musicAnalyzerTheme
    },
  },
});

export default vuetify;
