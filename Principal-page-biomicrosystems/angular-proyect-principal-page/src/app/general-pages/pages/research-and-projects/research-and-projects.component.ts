import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-research-and-projects',
  templateUrl: './research-and-projects.component.html',
  styleUrls: ['./research-and-projects.component.scss']
})
export class ResearchAndProjectsComponent implements OnInit {

  coll: HTMLCollectionOf<HTMLElement>;

  constructor() { }

  ngOnInit(): void {
    this.coll = document.getElementsByClassName("collapsible") as HTMLCollectionOf<HTMLElement>;
    this.addEventListeners();
  }

  addEventListeners() {
    for (let i = 0; i < this.coll.length; i++) {
      this.coll[i].addEventListener("click", () => {
        this.coll[i].classList.toggle("active");
        let content = this.coll[i].nextElementSibling as HTMLElement;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      });
    }
  }
}
