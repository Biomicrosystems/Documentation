import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from '../app-routing.module';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { AboutUsComponent } from './components/about-us/about-us.component';
import { HeaderComponent } from './components/header/header.component';
import { PrincipalPageComponent } from './pages/principal-page/principal-page.component';
import { LoginComponent } from './pages/login/login.component';
import { SectionProyectComponent } from './components/section-proyect/section-proyect.component';
import { SectionPublicationsComponent } from './components/section-publications/section-publications.component';
import { ResearchAndProjectsComponent } from './pages/research-and-projects/research-and-projects.component';
import { MembersComponent } from './pages/members/members.component';
import { ContactComponent } from './pages/contact/contact.component';


@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    AboutUsComponent,
    HeaderComponent,
    PrincipalPageComponent,
    LoginComponent,
    SectionProyectComponent,
    SectionPublicationsComponent,
    ResearchAndProjectsComponent,
    MembersComponent,
    ContactComponent
    ],
  imports: [
    CommonModule,
    AppRoutingModule
  ]
})
export class GeneralPagesModule { }
