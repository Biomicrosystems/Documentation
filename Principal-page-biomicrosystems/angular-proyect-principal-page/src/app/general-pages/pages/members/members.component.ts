import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.scss']
})
export class MembersComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    document.getElementById("defaultOpen")?.click();
  }

  openPage(pageName: string, elmnt: any, color: string) {
    let tabcontent = document.getElementsByClassName("tabcontent") as HTMLCollectionOf<HTMLElement>;
    for (let i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    let tablinks = document.getElementsByClassName("tablink") as HTMLCollectionOf<HTMLElement>;
    for (let i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = "";
    }

    let pageElement = document.getElementById(pageName);
    if (pageElement) {
      pageElement.style.display = "block";
    }

    elmnt.style.backgroundColor = color;
  }

}



