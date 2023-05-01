// vuetify.ts
import { createVuetify } from 'vuetify';
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import * as labs from 'vuetify/labs/components';
import { aliases, mdi } from 'vuetify/lib/iconsets/mdi-svg';
import {mdiMagnify} from '@mdi/js';
// import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

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
});

export default vuetify;
