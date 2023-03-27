import { Component } from '@angular/core';
// @ts-ignore
import * as L from 'leaflet';
import {Subscription} from "rxjs";
import {MunitionsService} from "./munitions/munitions.service";
import {PlatformsService} from "./platforms/platforms.service";
import {WindfarmsService} from "./windfarms/windfarms.service";
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  longitudeValue: any;
  latitudeValue: any;
  zonesSubs: Subscription = new Subscription();
  munitions: any[] = [];
  private munitions_group: any[] | undefined;
  private platforms: any[] | undefined;
  private platforms_group: any[] | undefined;
  private windfarms_group: any[] | undefined;
  private windfarms: any[] | undefined;
  constructor(private munitionsService: MunitionsService,
              private platformsService: PlatformsService,
              private windfarmService: WindfarmsService) {
  }

  submitForm(event: any) {
    console.log(event)
    console.log(this.longitudeValue, this.latitudeValue)
  }

  private map: any;


  ngOnInit() {
    this.munitionsService
      .getMunitions()
      .subscribe(res => {
        this.munitions = res;
          this.munitions_group = []
        // @ts-ignore
          for (const munition of this.munitions['features']){
          // @ts-ignore
            const circleCenter = munition['geometry']['coordinates'];
            const circleOptions = {
              color: '#da0000',
              fill: true,
              fillColor: '#da0000',
              fillOpacity: 0.5
            };
            const single_munition = L.circle([circleCenter[1], circleCenter[0]], 50, circleOptions);
            this.munitions_group.push(single_munition)
          }

        this.platformsService
          .getPlatforms()
          .subscribe(res => {
            this.platforms = res;
            this.platforms_group = []

            // @ts-ignore
            for (const platform of this.platforms['features']) {
              // @ts-ignore
              const circleCenter = platform['geometry']['coordinates'];
              const circleOptions = {
                color: '#fdf20a',
                fill: true,
                fillColor: '#fdf20a',
                fillOpacity: 0.5
              };
              const single_platform = L.circle([circleCenter[1], circleCenter[0]], 50, circleOptions);
              this.platforms_group.push(single_platform)
            }

              this.windfarmService
                .getWindfarms()
                .subscribe(res => {
                  this.windfarms = res;
                  this.windfarms_group = []

                  // @ts-ignore
                  for (const windfarm of this.windfarms['features']) {
                    // @ts-ignore
                    const polyOptions = {
                      color: '#08c600',
                      fill: true,
                      fillColor: '#08c600',
                      fillOpacity: 0.5
                    };

                    const polywind = []
                    console.log(windfarm['geometry']['coordinates'])
                    for (const coord1 of windfarm['geometry']['coordinates'] ) {
                      for (const coord2 of coord1) {
                        for (const points of coord1) {
                          for (const point of points) {
                            polywind.push([point[1], point[0]])
                          }

                        }
                      }
                    }

                    const single_windfarm = L.polygon(polywind, polyOptions);
                    this.windfarms_group.push(single_windfarm)
                  }
            const layer_group_munition = L.layerGroup(this.munitions_group);
            const layer_group_platform = L.layerGroup(this.platforms_group);
            const layer_group_windfarms = L.layerGroup(this.windfarms_group);

            const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              maxZoom: 18,
              minZoom: 3,
            });

            const satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
              maxZoom: 20,
              subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
            });

            this.map = L.map('map', {
              center: [52.080851, 2.887861],
              zoom: 7,
              layers: [tiles, layer_group_munition, layer_group_platform, layer_group_windfarms]
            });

            const baseMaps = {
              "Street view": tiles,
              "Satellite view": satellite
            };

            const overlayMaps = {
              "Munition": layer_group_munition,
              "Offshore platforms": layer_group_platform,
              "Windfarms": layer_group_windfarms
            };

            L.control.layers(baseMaps, overlayMaps).addTo(this.map);
          });
          });
              },
        console.error
      );

  }

  ngOnDestroy() {
  }

  ngAfterViewInit() {
  }
}
