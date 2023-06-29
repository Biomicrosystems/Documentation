import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PrincipalPageComponent } from './general-pages/pages/principal-page/principal-page.component';
import { ResearchAndProjectsComponent } from './general-pages/pages/research-and-projects/research-and-projects.component';
import { MembersComponent } from './general-pages/pages/members/members.component';
import { ContactComponent } from './general-pages/pages/contact/contact.component';


const routes: Routes = [
  {
    path: '',
    component: PrincipalPageComponent,
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
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
