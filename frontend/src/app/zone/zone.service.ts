import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Observable} from "rxjs";
import {Zone} from "./zone.model";
import {API_URL} from "../env";

@Injectable({
  providedIn: 'root'
})
export class ZoneService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(error: HttpErrorResponse) {
    throw new Error(error.message || 'Unable to retrieve songs');
  }

  getZones(): Observable<Zone[]> {
    try {
      return this.http
        .get<Zone[]>(`${API_URL}/zones`)
    } catch (error) {
      // @ts-ignore
      ZoneService._handleError(error);
      return new Observable<Zone[]>();
    }
  }
}
