import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  routerLink = ""
  constructor() { }

  ngOnInit(): void {
    const navLinks = document.querySelectorAll('.topnav a');

    navLinks.forEach(link => {
      link.addEventListener('click', (event) => {
        event.preventDefault();

        navLinks.forEach(link => {
          (link as HTMLElement).classList.remove('active-link');
        });

        (event.target as HTMLElement).classList.add('active-link');
      });
    });
  }

}
