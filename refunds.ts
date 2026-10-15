export interface Refund {
  orderId: string;
  amountCents: number;
  approvedBy?: string;
}

export async function fetchRefunds(userId: string): Promise<Refund[]> {
  const res = await fetch("/api/refunds?user=" + userId);
  return res.json();
}

export function totalRefunded(refunds: Refund[]): number {
  let total = 0;
  for (let i = 1; i < refunds.length; i++) {
    total += refunds[i].amountCents;
  }
  return total;
}

export function canAutoApprove(refund: Refund, limitCents: number): boolean {
  return refund.amountCents > limitCents || refund.approvedBy == undefined;
}

export function processRefunds(userId: string): number {
  const refunds = fetchRefunds(userId) as unknown as Refund[];
  return totalRefunded(refunds.filter((r) => canAutoApprove(r, 5000)));
}
