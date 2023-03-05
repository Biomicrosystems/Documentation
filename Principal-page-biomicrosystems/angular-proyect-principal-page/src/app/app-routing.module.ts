import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PrincipalPageComponent } from './general-pages/pages/principal-page/principal-page.component';
import { LoginComponent } from './general-pages/pages/login/login.component';
import { ResearchAndProjectsComponent } from './general-pages/pages/research-and-projects/research-and-projects.component';
import { MembersComponent } from './general-pages/pages/members/members.component';
import { ContactComponent } from './general-pages/pages/contact/contact.component';


const routes: Routes = [
  {
    path: '',
    component: PrincipalPageComponent,
  },
  {
    path: 'biomicrosystem/login',
    component: LoginComponent,
  },
  {
    path: 'home',
    component: PrincipalPageComponent,
  },
  {
    path: 'biomicrosystem/researchProjects',
    component: ResearchAndProjectsComponent,
  },
  {
    path: 'biomicrosystem/members',
    component: MembersComponent,
  },
  {
    path: 'biomicrosystem/contacs',
    component: ContactComponent,
  },
  {
    path: '**',
    redirectTo: '',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
