import { NextApiResponse, NextApiRequest } from 'next'
import { people } from '../../../data'
import { Person } from '../../../interfaces'

export default async function handler(
    _req: NextApiRequest,
    res: NextApiResponse<Person[]>
) {
  const data = await fetch(`http://127.0.0.1:5000/hello`);
  const [people] = await Promise.all([data]);
  return res.status(200).json(await people.json())
}
