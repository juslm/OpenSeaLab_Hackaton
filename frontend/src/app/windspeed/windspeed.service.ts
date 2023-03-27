import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Observable} from "rxjs";
import {API_URL} from "../env";

@Injectable({
  providedIn: 'root'
})
export class WindspeedService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(error: HttpErrorResponse) {
    throw new Error(error.message || 'Unable to retrieve offshore platforms');
  }

  getWindspeed(): Observable<any[]> {
    try {
      return this.http
        .get<any[]>(`${API_URL}/windspeed`)
    } catch (error) {
      // @ts-ignore
      WindspeedService._handleError(error);
      return new Observable<any[]>();
    }
  }
}
