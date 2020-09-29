import Vue from 'vue'
import Router from 'vue-router'
import home from "@/components/home";
import class_manage from "@/components/class_manage";
import project_manage from "@/components/project_manage";
import work_table from "@/components/work_table";
import help from "@/components/help";
import dashboard from "@/components/dashboard";
import external_page from "@/components/external_page";
import researcher from "@/components/researcher";
import researcher_entity from "@/components/researcher_entity";
import researcher_relation from "@/components/researcher_relation";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
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
        {path: 'researcher', name: 'researcher', component: researcher},
        {path: 'researcher_relation', name: 'researcher_relation', component: researcher_relation},
        {path: 'researcher_entity', name: 'researcher_entity', component: researcher_entity},
        {path: 'external_page', name: 'external_page', component: external_page},
        {path: 'work_table', name: 'work_table', component: work_table, meta:
            {ws_port: 'ws://10.10.2.85:8000/ws', pdf_port: 'http://10.10.2.85:8000/get_file/'}},
      ]
    },
  ]
})

