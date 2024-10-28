-- CreateTable
CREATE TABLE "StaticOption" (
    "id" SERIAL NOT NULL,
    "optionText" TEXT NOT NULL,
    "order" INTEGER NOT NULL,
    "surveyId" INTEGER NOT NULL,

    CONSTRAINT "StaticOption_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "StaticFactorImpact" (
    "id" SERIAL NOT NULL,
    "factorId" INTEGER NOT NULL,
    "staticOptionId" INTEGER NOT NULL,
    "impact" INTEGER NOT NULL,
    "plus" BOOLEAN NOT NULL,

    CONSTRAINT "StaticFactorImpact_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "StaticOption" ADD CONSTRAINT "StaticOption_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES "Survey"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StaticFactorImpact" ADD CONSTRAINT "StaticFactorImpact_factorId_fkey" FOREIGN KEY ("factorId") REFERENCES "Factor"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StaticFactorImpact" ADD CONSTRAINT "StaticFactorImpact_staticOptionId_fkey" FOREIGN KEY ("staticOptionId") REFERENCES "StaticOption"("id") ON DELETE CASCADE ON UPDATE CASCADE;
