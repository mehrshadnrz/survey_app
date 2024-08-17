/*
  Warnings:

  - You are about to drop the column `end_time` on the `Survey` table. All the data in the column will be lost.
  - You are about to drop the column `isPublic` on the `Survey` table. All the data in the column will be lost.
  - You are about to drop the column `start_time` on the `Survey` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Exam" ADD COLUMN     "creationDate" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "isPublic" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "viewableByAuthorOnly" BOOLEAN NOT NULL DEFAULT false;

-- AlterTable
ALTER TABLE "Survey" DROP COLUMN "end_time",
DROP COLUMN "isPublic",
DROP COLUMN "start_time";
