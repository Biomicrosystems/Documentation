import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GeneralPagesModule } from './general-pages/general-pages.module';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    GeneralPagesModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
