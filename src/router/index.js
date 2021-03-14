import Vue from 'vue'
import Router from 'vue-router'
import home from "@/components/home";
import class_manage from "@/components/class_manage";
import project_manage from "@/components/project_manage";
import work_table from "@/components/work_table";
import help from "@/components/help";
import dashboard from "@/components/dashboard";
import external_page from "@/components/external_page";
import researcher_beta from "@/components/researcher_beta";
import figures from "@/components/figures";
import qa_ner from "@/components/qa_ner";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home,
      children: [{path: '', name: 'dashboard', component: dashboard},]
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      children: [
        {path: 'class_manage', name: 'class_manage', component: class_manage},
        {path: 'project_manage', name: 'project_manage', component: project_manage},
        {path: 'help', name: 'help', component: help},
        {path: 'dashboard', name: 'dashboard', component: dashboard},
        {path: 'researcher_beta', name: 'researcher_beta', component: researcher_beta},
        {path: 'external_page', name: 'external_page', component: external_page},
        {path: 'figures', name: 'figures', component: figures, meta: {img_port: 'http://10.10.2.77:8000/get_file/'}},
        {path: 'qa_ner', name: 'qa_ner', component: qa_ner},
        {path: 'work_table', name: 'work_table', component: work_table, meta:
            {ws_port: 'ws://10.10.2.77:8000/ws', pdf_port: 'http://10.10.2.77:8000/get_file/'}},
      ]
    },
  ]
})

