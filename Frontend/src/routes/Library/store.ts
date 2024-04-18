// src/store.ts
import { writable } from 'svelte/store';

export interface UserInfo {
	userID: number;
	username: string;
	pass: string; // Consider not exposing passwords to the frontend
	category: string;
}

export interface TeamInfo {
	teamID: number;
	teamName: string;
}

export interface EquipmentInfo {
	equipmentID: number;
	equipName: string;
	unitPrice: number;
	initQuantity: number;
	currQuantity: number;
}

// Assuming players and coaches are a subset of user_info
export interface PlayerInfo {
	pID: number;
	tID: number;
}

export interface CoachInfo {
	coachID: number;
	tID: number;
}

export interface ActivityLog {
	cID: number;
	tID: number;
	eID: number;
	coDate: string;
	equipDiff: number;
}

// Define the overall structure for the orgData
export interface OrgData {
	coaches: CoachInfo[];
	equipment: EquipmentInfo[];
	players: PlayerInfo[];
	teams: TeamInfo[];
}

// Create a writable store with the type initialized with empty arrays
export const orgData = writable<OrgData>({
	coaches: [],
	equipment: [],
	players: [],
	teams: []
});
