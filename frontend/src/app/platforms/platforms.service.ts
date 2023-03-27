import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Observable} from "rxjs";
import {API_URL} from "../env";

@Injectable({
  providedIn: 'root'
})
export class PlatformsService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(error: HttpErrorResponse) {
    throw new Error(error.message || 'Unable to retrieve offshore platforms');
  }

  getPlatforms(): Observable<any[]> {
    try {
      return this.http
        .get<any[]>(`${API_URL}/platforms`)
    } catch (error) {
      // @ts-ignore
      PlatformsService._handleError(error);
      return new Observable<any[]>();
    }
  }
}
