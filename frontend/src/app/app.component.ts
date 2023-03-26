import { Component } from '@angular/core';
// @ts-ignore
import * as L from 'leaflet';
import {ZoneService} from "./zone/zone.service";
import {Subscription} from "rxjs";
import {Zone} from "./zone/zone.model";
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  longitudeValue: any;
  latitudeValue: any;
  zonesSubs: Subscription = new Subscription();
  zones: Zone[] = [];
  constructor(private zoneService: ZoneService) {
  }

  submitForm(event: any) {
    console.log(event)
    console.log(this.longitudeValue, this.latitudeValue)
  }

  private map: any;

  private initMap(): void {
    this.map = L.map('map', {
      center: [ 52.080851, 2.887861 ],
      zoom: 7
    });

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
    });

    tiles.addTo(this.map);
  }

  ngAfterViewInit(): void {
    this.initMap();
  }

  ngOnInit() {
    this.zonesSubs = this.zoneService
      .getZones()
      .subscribe(res => {
          this.zones = res;

          for (const zone of this.zones) {
            L.polygon(zone.polygon).addTo(this.map);
          }
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.zonesSubs.unsubscribe();
  }
}
