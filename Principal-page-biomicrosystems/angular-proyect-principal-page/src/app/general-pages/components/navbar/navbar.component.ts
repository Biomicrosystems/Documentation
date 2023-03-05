import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  routerLink=""
  constructor() { }

  ngOnInit(): void {
  }

  // redirectResearchProjects(){}
  // redirectMembers(){
  //   this.routerLink="members"
  // }
  // redirectContacs(){}


}
